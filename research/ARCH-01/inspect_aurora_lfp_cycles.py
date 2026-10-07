"""Summarize cycle and current-level anomalies in selected Aurora LFP files."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

EXPECTED_MD5 = "eaec9549b74b59d998e5138dab965b5d"
EXPECTED_SIZE = 2_507_129_091
SAMPLE_CELLS = ("ccid000217", "ccid000249")
SAMPLE_CYCLES = tuple(range(7))


def hash_file(path: Path, algorithm: str) -> str:
    """Compute a file digest with bounded memory use."""
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def summarize_cell(table: Any, cell_id: str) -> dict[str, Any]:
    """Summarize selected initial cycle values without exporting source rows."""
    frame = table.to_pandas()
    cycle_values = frame["cycle_dimensionless"].to_numpy()
    transitions = cycle_values[1:] != cycle_values[:-1]
    decreases = cycle_values[1:] < cycle_values[:-1]
    result: dict[str, Any] = {
        "cell_id": cell_id,
        "row_count": len(frame),
        "cycle_min": int(cycle_values.min()),
        "cycle_max": int(cycle_values.max()),
        "cycle_transition_count": int(transitions.sum()),
        "cycle_decrease_count": int(decreases.sum()),
        "return_to_zero_count": int(((cycle_values[1:] == 0) & (cycle_values[:-1] != 0)).sum()),
        "first_24_cycle_values": [int(value) for value in cycle_values[:24]],
        "test_time_decrease_count": int(frame["test_time_millisecond"].diff().lt(0).sum()),
        "current_voltage_by_initial_cycle": [],
    }
    for cycle in SAMPLE_CYCLES:
        rows = frame.loc[frame["cycle_dimensionless"] == cycle]
        if rows.empty:
            continue
        result["current_voltage_by_initial_cycle"].append(
            {
                "cycle_dimensionless": cycle,
                "row_count": len(rows),
                "current_min_milliamp": float(rows["current_ampere"].min() * 1000),
                "current_max_milliamp": float(rows["current_ampere"].max() * 1000),
                "voltage_min_v": float(rows["voltage_volt"].min()),
                "voltage_max_v": float(rows["voltage_volt"].max()),
            }
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    observed_md5 = hash_file(args.archive, "md5")
    if args.archive.stat().st_size != EXPECTED_SIZE or observed_md5 != EXPECTED_MD5:
        raise SystemExit("Aurora archive does not match the selected Zenodo v1 artifact")
    with zipfile.ZipFile(args.archive) as archive:
        cells: list[dict[str, Any]] = []
        for cell_id in SAMPLE_CELLS:
            member = f"empa__{cell_id}/empa__{cell_id}.bdf.parquet"
            if member not in archive.namelist():
                raise SystemExit(f"Expected Aurora member is missing: {member}")
            with archive.open(member) as stream:
                table = pq.read_table(
                    stream,
                    columns=[
                        "test_time_millisecond",
                        "current_ampere",
                        "voltage_volt",
                        "cycle_dimensionless",
                    ],
                )
            cells.append(summarize_cell(table, cell_id))

    result = {
        "archive": {
            "size_bytes": args.archive.stat().st_size,
            "record_md5": EXPECTED_MD5,
            "observed_md5": observed_md5,
            "sha256": hash_file(args.archive, "sha256"),
        },
        "pyarrow_version": __import__("pyarrow").__version__,
        "cells": cells,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Inspected {len(cells)} Aurora LFP cycle streams; wrote {args.output}")


if __name__ == "__main__":
    main()
