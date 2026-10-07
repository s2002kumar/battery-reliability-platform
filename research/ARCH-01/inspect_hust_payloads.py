"""Safely inspect selected HUST pickle payloads with a strict class allowlist."""

from __future__ import annotations

import argparse
import builtins
import hashlib
import importlib
import json
import pickle
import statistics
import zipfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

EXPECTED_SHA256 = "071d24617153693b0d29059568525e620f6af6512acc9d00c98c7adcf15125db"
ALLOWED_GLOBALS = {
    ("builtins", "slice"),
    ("numpy", "dtype"),
    ("numpy", "ndarray"),
    ("numpy.core.multiarray", "_reconstruct"),
    ("numpy.core.multiarray", "scalar"),
    ("pandas.core.frame", "DataFrame"),
    ("pandas.core.indexes.base", "Index"),
    ("pandas.core.indexes.base", "_new_Index"),
    ("pandas.core.indexes.range", "RangeIndex"),
    ("pandas.core.internals.managers", "BlockManager"),
}


class RestrictedUnpickler(pickle.Unpickler):
    """Resolve only NumPy/pandas/builtins globals observed in static inspection."""

    def find_class(self, module: str, name: str) -> Any:
        if (module, name) not in ALLOWED_GLOBALS:
            raise pickle.UnpicklingError(f"Disallowed pickle global: {module}.{name}")
        if module == "builtins":
            return getattr(builtins, name)
        return getattr(importlib.import_module(module), name)


def sha256_file(path: Path) -> str:
    """Hash an input archive with bounded memory use."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def scalar(value: Any) -> Any:
    """Convert NumPy scalars and pandas missing values to JSON-safe values."""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def summarize_mapping(value: Any, *, include_early_statistics: bool = True) -> dict[str, Any]:
    """Report map key/value structure without persisting the full source label."""
    if isinstance(value, pd.Series):
        mapping = value.to_dict()
    elif isinstance(value, Mapping):
        mapping = value
    else:
        return {
            "type": type(value).__name__,
            "length": len(value) if hasattr(value, "__len__") else None,
        }

    keys = list(mapping.keys())
    numeric_items = [
        (scalar(key), float(scalar(mapping[key])))
        for key in keys
        if isinstance(scalar(mapping[key]), (int, float))
    ]
    early_windows: dict[str, Any] = {}
    if numeric_items and include_early_statistics:
        first_value = numeric_items[0][1]
        for window_size in (1, 3, 5, 10, 30):
            sample = [item[1] for item in numeric_items[:window_size]]
            median_value = statistics.median(sample)
            early_windows[str(window_size)] = {
                "count": len(sample),
                "median": median_value,
                "mean": statistics.fmean(sample),
                "min": min(sample),
                "max": max(sample),
                "range": max(sample) - min(sample),
                "population_sd": statistics.pstdev(sample),
                "first_vs_median_percent": (
                    100.0 * (first_value - median_value) / median_value
                    if median_value != 0
                    else None
                ),
            }
    return {
        "type": type(value).__name__,
        "length": len(keys),
        "key_type_counts": pd.Series([type(key).__name__ for key in keys]).value_counts().to_dict(),
        "first_key": scalar(keys[0]) if keys else None,
        "last_key": scalar(keys[-1]) if keys else None,
        "early_window_statistics": early_windows,
    }


def inspect_frame(frame: pd.DataFrame) -> dict[str, Any]:
    """Summarize observed row columns, signs, cycles, and capacity progress."""
    result: dict[str, Any] = {
        "shape": list(frame.shape),
        "columns": [str(column) for column in frame.columns],
        "dtypes": {str(name): str(dtype) for name, dtype in frame.dtypes.items()},
        "null_counts": {str(name): int(count) for name, count in frame.isna().sum().items()},
        "status_counts": {
            str(name): int(count)
            for name, count in frame["Status"].value_counts(dropna=False).items()
        },
    }
    if "Current (mA)" in frame:
        current = frame.groupby("Status", dropna=False)["Current (mA)"].agg(["min", "max", "mean"])
        result["current_by_status_mA"] = {
            str(status): {str(key): scalar(value) for key, value in row.items()}
            for status, row in current.iterrows()
        }
    if "Cycle number" in frame:
        result["cycle_number"] = {
            "count": int(frame["Cycle number"].nunique(dropna=True)),
            "min": scalar(frame["Cycle number"].min()),
            "max": scalar(frame["Cycle number"].max()),
            "null_rows": int(frame["Cycle number"].isna().sum()),
        }
    if {"Cycle number", "Status", "Capacity (mAh)"}.issubset(frame.columns):
        capacities = frame.groupby(["Cycle number", "Status"], dropna=False)["Capacity (mAh)"].agg(
            ["min", "max", "last"]
        )
        result["capacity_by_cycle_status_mAh"] = [
            {
                "cycle_number": scalar(cycle),
                "status": str(status),
                "min": scalar(row["min"]),
                "max": scalar(row["max"]),
                "last": scalar(row["last"]),
            }
            for (cycle, status), row in capacities.iterrows()
        ]
    return result


def inspect_cycle_data(value: Any) -> dict[str, Any]:
    """Summarize a cycle-keyed data mapping without assuming its key convention."""
    if isinstance(value, pd.DataFrame):
        frames = [(None, value)]
        container_type = "DataFrame"
    elif isinstance(value, Mapping):
        frames = list(value.items())
        container_type = type(value).__name__
    else:
        raise TypeError(f"Unsupported data container type: {type(value).__name__}")

    cycle_summaries: list[dict[str, Any]] = []
    schema_counts: dict[str, int] = {}
    total_rows = 0
    null_counts: dict[str, int] = {}
    current_ranges: dict[str, dict[str, float]] = {}
    cycle_key_matches = 0
    cycle_key_mismatches = 0
    for key, frame in frames:
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(
                f"Expected a DataFrame for cycle key {key!r}; observed {type(frame).__name__}"
            )
        frame_summary = inspect_frame(frame)
        observed_cycle = frame_summary.get("cycle_number")
        if (
            key is not None
            and observed_cycle is not None
            and observed_cycle["count"] == 1
            and observed_cycle["min"] == scalar(key)
            and observed_cycle["max"] == scalar(key)
            and observed_cycle["null_rows"] == 0
        ):
            cycle_key_matches += 1
        else:
            cycle_key_mismatches += 1
        total_rows += len(frame)
        for name, count in frame_summary["null_counts"].items():
            null_counts[name] = null_counts.get(name, 0) + count
        for status, stats in frame_summary.get("current_by_status_mA", {}).items():
            bounds = current_ranges.setdefault(status, {"min": float("inf"), "max": float("-inf")})
            bounds["min"] = min(bounds["min"], float(stats["min"]))
            bounds["max"] = max(bounds["max"], float(stats["max"]))
        frame_capacity = frame["Capacity (mAh)"] if "Capacity (mAh)" in frame else None
        schema = json.dumps(frame_summary["columns"], separators=(",", ":"))
        schema_counts[schema] = schema_counts.get(schema, 0) + 1
        cycle_summaries.append(
            {
                "container_key": scalar(key),
                "shape": frame_summary["shape"],
                "cycle_number": frame_summary.get("cycle_number"),
                "status_counts": frame_summary["status_counts"],
                "capacity_range_mAh": (
                    {
                        "min": scalar(frame_capacity.min()),
                        "max": scalar(frame_capacity.max()),
                        "range": scalar(frame_capacity.max() - frame_capacity.min()),
                    }
                    if frame_capacity is not None
                    else None
                ),
                "capacity_by_cycle_status_mAh": frame_summary.get(
                    "capacity_by_cycle_status_mAh", []
                ),
                "current_by_status_mA": frame_summary.get("current_by_status_mA", {}),
            }
        )
    return {
        "container_type": container_type,
        "entry_count": len(cycle_summaries),
        "total_rows": total_rows,
        "column_schema_counts": schema_counts,
        "null_counts": null_counts,
        "current_ranges_mA_by_status": current_ranges,
        "cycle_key_semantics": {
            "matching_frames": cycle_key_matches,
            "mismatching_or_unverifiable_frames": cycle_key_mismatches,
        },
        "entries": cycle_summaries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--members",
        nargs="+",
        default=[
            "our_data/1-1.pkl",
            "our_data/2-2.pkl",
            "our_data/5-7.pkl",
            "our_data/6-8.pkl",
            "our_data/10-8.pkl",
        ],
    )
    arguments = parser.parse_args()

    observed_sha256 = sha256_file(arguments.archive)
    if observed_sha256 != EXPECTED_SHA256:
        raise SystemExit(f"HUST archive checksum mismatch: {observed_sha256}")

    payloads: dict[str, Any] = {}
    with zipfile.ZipFile(arguments.archive) as archive:
        available = set(archive.namelist())
        for member_name in arguments.members:
            if member_name not in available:
                raise SystemExit(f"Expected HUST archive member is missing: {member_name}")
            with archive.open(member_name) as member:
                payload = RestrictedUnpickler(member).load()
            if not isinstance(payload, Mapping) or len(payload) != 1:
                raise SystemExit(f"Unexpected top-level pickle shape in {member_name}")

            cell_key, cell_data = next(iter(payload.items()))
            if not isinstance(cell_data, Mapping):
                raise SystemExit(f"Unexpected cell object type in {member_name}")
            observed_keys = {str(key) for key in cell_data.keys()}
            if not {"data", "dq", "rul"}.issubset(observed_keys):
                raise SystemExit(f"Missing expected payload keys in {member_name}: {observed_keys}")
            data_summary = inspect_cycle_data(cell_data["data"])
            dq_mapping = (
                cell_data["dq"].to_dict()
                if isinstance(cell_data["dq"], pd.Series)
                else cell_data["dq"]
            )
            if not isinstance(dq_mapping, Mapping) or not isinstance(cell_data["data"], Mapping):
                raise SystemExit(f"Expected cycle-keyed dq and data mappings in {member_name}")
            comparisons: list[dict[str, Any]] = []
            for cycle_key, frame in cell_data["data"].items():
                if not isinstance(frame, pd.DataFrame) or cycle_key not in dq_mapping:
                    continue
                capacity_series = frame["Capacity (mAh)"]
                peak_capacity = capacity_series.max()
                final_capacity = capacity_series.iloc[-1]
                peak_to_final = peak_capacity - final_capacity
                dq_value = float(dq_mapping[cycle_key])
                comparisons.append(
                    {
                        "cycle_key": scalar(cycle_key),
                        "dq_mAh": dq_value,
                        "peak_capacity_mAh": scalar(peak_capacity),
                        "final_capacity_mAh": scalar(final_capacity),
                        "peak_to_final_mAh": scalar(peak_to_final),
                        "absolute_difference_mAh": scalar(abs(dq_value - peak_to_final)),
                    }
                )

            differences = [item["absolute_difference_mAh"] for item in comparisons]
            compact_data = {
                "container_type": data_summary["container_type"],
                "entry_count": data_summary["entry_count"],
                "total_rows": data_summary["total_rows"],
                "column_schema_counts": data_summary["column_schema_counts"],
                "null_counts": data_summary["null_counts"],
                "current_ranges_mA_by_status": data_summary["current_ranges_mA_by_status"],
                "cycle_key_semantics": data_summary["cycle_key_semantics"],
                "status_values": sorted(
                    {
                        status
                        for entry in data_summary["entries"]
                        for status in entry["status_counts"]
                    }
                ),
                "all_cycle_frames_share_schema": len(data_summary["column_schema_counts"]) == 1,
            }
            payloads[member_name] = {
                "top_level_key": scalar(cell_key),
                "cell_object_keys": sorted(observed_keys),
                "dq": summarize_mapping(cell_data["dq"]),
                "rul": summarize_mapping(cell_data["rul"], include_early_statistics=False),
                "data": compact_data,
                "dq_vs_peak_minus_final_capacity": {
                    "matched_cycle_count": len(comparisons),
                    "max_absolute_difference_mAh": max(differences, default=None),
                    "median_absolute_difference_mAh": (
                        statistics.median(differences) if differences else None
                    ),
                },
            }

    result = {
        "archive_sha256": observed_sha256,
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "allowed_pickle_globals": [list(item) for item in sorted(ALLOWED_GLOBALS)],
        "members": payloads,
        "restricted_unpickler": True,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"Safely inspected {len(payloads)} payloads; wrote {arguments.output}")


if __name__ == "__main__":
    main()
