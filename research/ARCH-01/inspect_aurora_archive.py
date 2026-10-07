"""Audit the exact Aurora Zenodo v1 archive without extracting source bytes."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

EXPECTED_MD5 = "eaec9549b74b59d998e5138dab965b5d"
EXPECTED_SIZE = 2_507_129_091
EXPECTED_CELLS = 199


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def find_formula(node: Any) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if "molecularFormula" in node:
            formula = node["molecularFormula"]
            if isinstance(formula, dict):
                value = formula.get("rdfs:comment")
                if isinstance(value, str):
                    found.append(value)
        for value in node.values():
            found.extend(find_formula(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(find_formula(value))
    return found


def find_typed_values(node: Any, wanted_type: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if wanted_type in types:
            found.append(node)
        for value in node.values():
            found.extend(find_typed_values(value, wanted_type))
    elif isinstance(node, list):
        for value in node:
            found.extend(find_typed_values(value, wanted_type))
    return found


def summarize_meta(doc: dict[str, Any], cell_id: str) -> dict[str, Any]:
    graph = doc.get("@graph")
    if not isinstance(graph, list) or not graph:
        raise ValueError(f"{cell_id}: missing @graph")
    test = next((n for n in graph if n.get("@type") == "BatteryTest"), None)
    if test is None:
        raise ValueError(f"{cell_id}: missing BatteryTest")
    obj = test.get("hasTestObject", {})
    product_ids = obj.get("schema:productID", [])
    formulas = find_formula(test)
    formula_blob = " ".join(formulas).lower()
    pos = test.get("hasPositiveElectrode", {})
    neg = obj.get("hasNegativeElectrode", {})
    pos_name = " ".join(find_text(pos)).lower()
    neg_name = " ".join(find_text(neg)).lower()
    if "lifepo4" in pos_name or "lifepo4" in formula_blob:
        chemistry = "LFP/graphite" if "graphite" in neg_name else "LFP/negative-unverified"
    elif "lini0.6co0.2mn0.2o2" in formula_blob:
        chemistry = "NMC622/graphite" if "graphite" in neg_name else "NMC622/negative-unverified"
    elif "ni0.83mn0.06co0.11o2" in formula_blob:
        chemistry = (
            "NMC-Ni0.83Mn0.06Co0.11/graphite"
            if "graphite" in neg_name
            else "NMC-Ni0.83Mn0.06Co0.11/negative-unverified"
        )
    else:
        chemistry = "unclassified"
    return {
        "cell_id": cell_id,
        "product_ids": product_ids,
        "date_created": obj.get("schema:dateCreated"),
        "creator": (obj.get("schema:creator") or {}).get("schema:name"),
        "chemistry": chemistry,
        "positive_formulas": sorted(set(formulas)),
        "negative_electrode_types": sorted(set(find_text(neg))),
        "rated_capacity_properties": find_typed_values(test, "RatedCapacity"),
        "protocol_types": sorted(
            {
                t
                for n in find_typed_values(test, "ConstantCurrentConstantVoltageCycling")
                for t in (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])
            }
        ),
        "protocol_task_tree": find_typed_values(test, "Charging")
        + find_typed_values(test, "Discharging"),
        "comments": obj.get("rdfs:comment", []),
    }


def find_text(node: Any) -> list[str]:
    vals: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in {"@type", "rdfs:comment", "schema:name", "rdfs:label"}:
                if isinstance(value, str):
                    vals.append(value)
                elif isinstance(value, list):
                    vals.extend(v for v in value if isinstance(v, str))
                elif isinstance(value, dict):
                    vals.extend(find_text(value))
            else:
                vals.extend(find_text(value))
    elif isinstance(node, list):
        for value in node:
            vals.extend(find_text(value))
    return vals


def _column_stat(parquet: pq.ParquetFile, column_index: int, attribute: str) -> Any:
    values = [
        getattr(parquet.metadata.row_group(group).column(column_index).statistics, attribute)
        for group in range(parquet.metadata.num_row_groups)
        if parquet.metadata.row_group(group).column(column_index).statistics is not None
    ]
    if not values:
        return None
    return min(values) if attribute == "min" else max(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive
    md5 = digest(archive, "md5")
    sha256 = digest(archive, "sha256")
    if archive.stat().st_size != EXPECTED_SIZE or md5 != EXPECTED_MD5:
        raise SystemExit("archive does not match the selected Zenodo v1 artifact")

    result: dict[str, Any] = {
        "archive": {
            "size_bytes": archive.stat().st_size,
            "md5": md5,
            "sha256": sha256,
            "recorded_md5": EXPECTED_MD5,
        },
        "environment": {"pyarrow": __import__("pyarrow").__version__},
    }
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        files = [n for n in names if not n.endswith("/")]
        ids = sorted(
            {match.group(1) for name in files if (match := re.match(r"empa__(ccid\d{6})/", name))}
        )
        if len(ids) != EXPECTED_CELLS or len(names) != 797:
            raise SystemExit(f"unexpected crate inventory: entries={len(names)}, cells={len(ids)}")
        suffixes = Counter(Path(n).suffix for n in files)
        expected_files = {
            f"empa__{cell}/empa__{cell}{suffix}"
            for cell in ids
            for suffix in (".metadata.json", ".bdf.csv", ".bdf.parquet")
        }
        missing = sorted(expected_files - set(files))
        extra = sorted(set(files) - expected_files - {"ro-crate-metadata.json"})
        if missing or extra:
            raise SystemExit(f"unexpected members: missing={missing[:5]}, extra={extra[:5]}")

        cells: list[dict[str, Any]] = []
        schema_counts: Counter[str] = Counter()
        rows_total = 0
        cycle_ranges: dict[str, list[int]] = {}
        for cell in ids:
            prefix = f"empa__{cell}/empa__{cell}"
            meta = json.loads(zf.read(prefix + ".metadata.json"))
            item = summarize_meta(meta, cell)
            with zf.open(prefix + ".bdf.parquet") as stream:
                parquet = pq.ParquetFile(stream)
                schema_string = str(parquet.schema_arrow)
                schema_counts[schema_string] += 1
                rows_total += parquet.metadata.num_rows
                table = parquet.read(columns=["cycle_dimensionless"])
                cycles = table.column(0).drop_null().to_numpy()
                cycle_ranges[cell] = [int(cycles.min()), int(cycles.max())] if len(cycles) else []
                item["parquet_rows"] = parquet.metadata.num_rows
                item["cycle_min_max"] = cycle_ranges[cell]
                transitions = cycles[1:] != cycles[:-1]
                decreases = cycles[1:] < cycles[:-1]
                item["cycle_sequence_audit"] = {
                    "transition_count": int(transitions.sum()),
                    "decrease_count": int(decreases.sum()),
                    "return_to_zero_count": int(((cycles[1:] == 0) & (cycles[:-1] != 0)).sum()),
                    "first_values": [int(value) for value in cycles[:20]],
                }
                item["parquet_schema"] = schema_string
                item["parquet_column_statistics"] = {
                    field.name: {
                        "null_count": sum(
                            (
                                parquet.metadata.row_group(group)
                                .column(index)
                                .statistics.null_count
                                or 0
                            )
                            for group in range(parquet.metadata.num_row_groups)
                        ),
                        "min": _column_stat(parquet, index, "min"),
                        "max": _column_stat(parquet, index, "max"),
                    }
                    for index, field in enumerate(parquet.schema_arrow)
                }
            cells.append(item)

        chemistry_counts = Counter(cell["chemistry"] for cell in cells)
        # CSV/Parquet are directly compared for first and last IDs of each chemistry.
        comparison: list[dict[str, Any]] = []
        selected: set[str] = set()
        for chemistry in sorted(chemistry_counts):
            matching = [cell["cell_id"] for cell in cells if cell["chemistry"] == chemistry]
            if matching:
                selected.update((matching[0], matching[-1]))
        for cell in sorted(selected):
            prefix = f"empa__{cell}/empa__{cell}"
            with zf.open(prefix + ".bdf.csv") as raw:
                csv_bytes = raw.read()
            csv_table = __import__("pyarrow.csv", fromlist=["read_csv"]).read_csv(
                io.BytesIO(csv_bytes)
            )
            with zf.open(prefix + ".bdf.parquet") as raw:
                parquet_table = pq.read_table(raw)
            identical = csv_table.schema.equals(parquet_table.schema) and csv_table.equals(
                parquet_table
            )
            comparison.append(
                {
                    "cell_id": cell,
                    "csv_rows": csv_table.num_rows,
                    "parquet_rows": parquet_table.num_rows,
                    "csv_columns": csv_table.column_names,
                    "parquet_columns": parquet_table.column_names,
                    "schema_equal": csv_table.schema.equals(parquet_table.schema),
                    "values_equal": identical,
                }
            )

    result["inventory"] = {
        "entry_count_including_directories": 797,
        "file_suffix_counts": dict(suffixes),
        "cell_count": len(cells),
        "chemistry_counts": dict(chemistry_counts),
        "cell_ids": ids,
        "lfp_cell_ids": [c["cell_id"] for c in cells if c["chemistry"].startswith("LFP/")],
        "total_parquet_rows": rows_total,
        "unique_parquet_schemas": len(schema_counts),
        "schema_cell_counts": [
            {"count": count, "schema": schema} for schema, count in schema_counts.items()
        ],
        "cycle_min_max_by_cell": cycle_ranges,
        "cycle_anomaly_totals_by_chemistry": {
            chemistry: {
                "cells": sum(cell["chemistry"] == chemistry for cell in cells),
                "decrease_count": sum(
                    cell["cycle_sequence_audit"]["decrease_count"]
                    for cell in cells
                    if cell["chemistry"] == chemistry
                ),
                "return_to_zero_count": sum(
                    cell["cycle_sequence_audit"]["return_to_zero_count"]
                    for cell in cells
                    if cell["chemistry"] == chemistry
                ),
            }
            for chemistry in sorted(chemistry_counts)
        },
        "csv_parquet_comparison": comparison,
        "cells": cells,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "archive": result["archive"],
                "inventory": {
                    key: value
                    for key, value in result["inventory"].items()
                    if key not in {"cells", "cycle_min_max_by_cell", "schema_cell_counts"}
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
