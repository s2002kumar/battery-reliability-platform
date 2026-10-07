"""Audit the Aurora LFP metadata protocol against recorded BDF rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.parquet as pq

EXPECTED_MD5 = "eaec9549b74b59d998e5138dab965b5d"
EXPECTED_SHA256 = "61f66d309462c5bcbb00ddfef0d141ad836f811f2b78d07457aadc4a3e7baff7"
LFPS = [
    *(f"ccid{number:06d}" for number in range(217, 248) if number != 248),
    "ccid000249",
]
REQUIRED_COLUMNS = {
    "test_time_millisecond",
    "current_ampere",
    "voltage_volt",
    "cycle_dimensionless",
    "date_time_millisecond",
    "ambient_temperature_celsius",
}


def file_hash(path: Path, algorithm: str) -> str:
    """Hash a source archive using bounded memory."""
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def types(value: Any) -> list[str]:
    """Normalize an ontology type value to strings."""
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)] if value is not None else []


def parameters(node: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract direct task inputs without traversing linked metadata."""
    output: list[dict[str, Any]] = []
    inputs = node.get("hasInput", [])
    if isinstance(inputs, dict):
        inputs = [inputs]
    if not isinstance(inputs, list):
        return output
    for item in inputs:
        if not isinstance(item, dict):
            continue
        numeric = item.get("hasNumericalPart", {})
        output.append(
            {
                "type": types(item.get("@type")),
                "value": numeric.get("hasNumberValue") if isinstance(numeric, dict) else None,
                "unit": item.get("hasMeasurementUnit"),
            }
        )
    return output


def summarize_procedure(node: Any) -> list[dict[str, Any]]:
    """Flatten task order and iteration counts from one BatteryTest procedure."""
    tasks: list[dict[str, Any]] = []

    def walk(task: Any, path: str) -> None:
        if not isinstance(task, dict):
            return
        task_types = types(task.get("@type"))
        inputs = parameters(task)
        if task_types:
            tasks.append({"path": path, "type": task_types, "inputs": inputs})
        iterations = next(
            (
                item["value"]
                for item in inputs
                if "NumberOfIterations" in item["type"] and item["value"] is not None
            ),
            None,
        )
        if "hasTask" in task:
            walk(task["hasTask"], f"{path}/hasTask" + (f"*{iterations}" if iterations else ""))
        if "hasNext" in task:
            walk(task["hasNext"], f"{path}/hasNext")

    procedure = node.get("hasMeasurementParameter")
    if isinstance(procedure, dict):
        walk(procedure.get("hasTask"), "procedure/hasTask")
    return tasks


def metadata_audit(raw: bytes, cell_id: str) -> dict[str, Any]:
    """Read direct per-cell BatteryTest metadata, excluding reverse links."""
    document = json.loads(raw)
    graph = document.get("@graph")
    tests = [
        item
        for item in graph
        if isinstance(item, dict) and "BatteryTest" in types(item.get("@type"))
    ]
    if len(tests) != 1:
        raise ValueError(f"Expected one direct BatteryTest node for {cell_id}; got {len(tests)}")
    test = tests[0]
    cell = test.get("hasTestObject", {})
    procedure = test.get("hasMeasurementParameter", {})
    return {
        "cell_id": cell_id,
        "chemistry_formula": cell.get("hasPositiveElectrode", {})
        .get("hasCoating", {})
        .get("hasActiveMaterial", {})
        .get("molecularFormula", {})
        .get("rdfs:comment"),
        "cell_type": types(cell.get("@type")),
        "product_ids": cell.get("schema:productID"),
        "protocol_types": types(procedure.get("@type")) if isinstance(procedure, dict) else [],
        "procedure_tasks": summarize_procedure(test),
        "rated_capacity_properties": [
            {
                "value": item.get("hasNumericalPart", {}).get("hasNumberValue"),
                "unit": item.get("hasMeasurementUnit"),
            }
            for item in cell.get("hasPositiveElectrode", {}).get("hasMeasuredProperty", [])
            if isinstance(item, dict)
            and "RatedCapacity" in types(item.get("@type"))
            and isinstance(item.get("hasNumericalPart"), dict)
        ],
    }


def contiguous_runs(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return inclusive start/end positions for true runs in a boolean vector."""
    padded = np.concatenate(([False], mask, [False]))
    changes = np.flatnonzero(padded[1:] != padded[:-1])
    return changes[::2], changes[1::2] - 1


def row_audit(raw: bytes, cell_id: str, expected_schema: str | None) -> dict[str, Any]:
    """Summarize measured row timing, signed-current runs, and discharge integration."""
    from io import BytesIO

    table = pq.read_table(BytesIO(raw))
    names = set(table.column_names)
    if names != REQUIRED_COLUMNS:
        raise ValueError(f"Unexpected BDF fields for {cell_id}: {sorted(names)}")
    schema = str(table.schema.remove_metadata())
    if expected_schema is not None and schema != expected_schema:
        raise ValueError(f"Schema mismatch for {cell_id}")
    if any(table.column(name).null_count for name in table.column_names):
        raise ValueError(f"Null BDF values found for {cell_id}")

    test_time = table.column("test_time_millisecond").combine_chunks().to_numpy()
    current = table.column("current_ampere").combine_chunks().to_numpy()
    voltage = table.column("voltage_volt").combine_chunks().to_numpy()
    cycle = table.column("cycle_dimensionless").combine_chunks().to_numpy()
    if not np.all(np.diff(test_time) >= 0):
        raise ValueError(f"Non-monotonic test_time_millisecond for {cell_id}")

    negative = current < 0
    starts, ends = contiguous_runs(negative)
    delta_time = np.diff(test_time.astype(np.float64))
    discharge_current = np.maximum(-current.astype(np.float64), 0.0)
    interval_capacity_ah = (
        0.5 * (discharge_current[:-1] + discharge_current[1:]) * delta_time / 3_600_000.0
    )
    run_capacities: list[float] = []
    run_stats: list[dict[str, float]] = []
    for start, end in zip(starts, ends, strict=True):
        interval_start = max(int(start) - 1, 0)
        interval_end = min(int(end), len(interval_capacity_ah) - 1)
        capacity_ah = float(interval_capacity_ah[interval_start : interval_end + 1].sum())
        run_capacities.append(capacity_ah * 1000.0)
        run_stats.append(
            {
                "capacity_mAh": capacity_ah * 1000.0,
                "mean_abs_current_mA": float(np.mean(-current[start : end + 1]) * 1000.0),
                "start_voltage_v": float(voltage[start]),
                "end_voltage_v": float(voltage[end]),
                "duration_s": float((test_time[end] - test_time[start]) / 1000.0),
            }
        )

    current_sign = np.sign(current).astype(np.int8)
    nonzero_sign = current_sign[current_sign != 0]
    sign_change_count = int(np.count_nonzero(np.diff(nonzero_sign)))
    reset_positions = np.flatnonzero((cycle[1:] == 0) & (cycle[:-1] > 0)) + 1
    lower_cutoff_count = sum(abs(item["end_voltage_v"] - 2.5) <= 0.08 for item in run_stats)
    substantial_runs = [item for item in run_stats if item["capacity_mAh"] >= 0.1]
    small_runs = [item["capacity_mAh"] for item in run_stats if item["capacity_mAh"] < 0.1]
    complete_capacities = [item["capacity_mAh"] for item in substantial_runs]
    formation = substantial_runs[:3]
    formation_capacities = [item["capacity_mAh"] for item in formation]
    aging_capacities = complete_capacities[3:]
    first_aging_capacity = aging_capacities[0] if aging_capacities else None
    aging_window_summaries: dict[str, dict[str, float]] = {}
    for window_size in (3, 5, 10):
        window = aging_capacities[:window_size]
        window_median = statistics.median(window) if window else 0.0
        aging_window_summaries[str(window_size)] = {
            "count": len(window),
            "median_capacity_mAh": window_median,
            "first_aging_vs_window_median_percent": (
                100.0 * (aging_capacities[0] - window_median) / window_median
                if window_median
                else 0.0
            ),
            "window_range_percent_of_median": (
                100.0 * (max(window) - min(window)) / window_median if window_median else 0.0
            ),
        }
    formation_median = statistics.median(formation_capacities) if formation_capacities else 0.0
    return {
        "cell_id": cell_id,
        "row_count": table.num_rows,
        "schema": schema,
        "time_monotonic_non_decreasing": True,
        "temperature_c_min": float(
            table.column("ambient_temperature_celsius").combine_chunks().to_numpy().min()
        ),
        "temperature_c_max": float(
            table.column("ambient_temperature_celsius").combine_chunks().to_numpy().max()
        ),
        "cycle_dimensionless_min": int(cycle.min()),
        "cycle_dimensionless_max": int(cycle.max()),
        "cycle_dimensionless_return_to_zero_count": int(len(reset_positions)),
        "current_sign_change_count_ignoring_zero": sign_change_count,
        "contiguous_negative_current_run_count": len(run_stats),
        "negative_runs_ending_within_0p08V_of_2p5V": lower_cutoff_count,
        "negative_runs_capacity_at_least_0p1mAh_count": len(substantial_runs),
        "max_negative_run_capacity_below_0p1mAh": max(small_runs, default=0.0),
        "min_negative_run_capacity_at_least_0p1mAh": min(
            (item["capacity_mAh"] for item in substantial_runs), default=0.0
        ),
        "substantial_run_count_ending_within_0p08V_of_2p5V": sum(
            abs(item["end_voltage_v"] - 2.5) <= 0.08 for item in substantial_runs
        ),
        "negative_run_current_magnitude_mA_min_max": [
            min(item["mean_abs_current_mA"] for item in run_stats),
            max(item["mean_abs_current_mA"] for item in run_stats),
        ],
        "first_three_negative_run_capacity_mAh": formation_capacities,
        "first_three_capacity_median_mAh": formation_median,
        "first_three_capacity_range_percent_of_median": (
            100.0 * (max(formation_capacities) - min(formation_capacities)) / formation_median
            if formation_median
            else None
        ),
        "first_three_mean_current_magnitude_mA": [
            item["mean_abs_current_mA"] for item in formation
        ],
        "first_three_formation_run_end_voltage_v": [item["end_voltage_v"] for item in formation],
        "first_three_formation_discharge_run_capacity_mAh": formation_capacities,
        "first_three_formation_cycle_count": len(formation),
        "first_aging_capacity_mAh": first_aging_capacity,
        "first_three_aging_run_end_voltage_v": [
            item["end_voltage_v"] for item in substantial_runs[3:6]
        ],
        "first_three_aging_discharge_capacity_mAh": [
            item["capacity_mAh"] for item in substantial_runs[3:6]
        ],
        "first_aging_capacity_vs_formation_median_percent": (
            100.0 * (first_aging_capacity - formation_median) / formation_median
            if first_aging_capacity is not None and formation_median
            else None
        ),
        "aging_reference_window_candidates": aging_window_summaries,
        "first_seven_aging_mean_current_magnitude_mA": [
            item["mean_abs_current_mA"] for item in substantial_runs[3:10]
        ],
        "negative_run_capacity_count": len(run_capacities),
        "negative_run_capacity_mAh_range": [min(run_capacities), max(run_capacities)],
        "negative_run_capacity_mAh_quantiles": [
            float(np.quantile(run_capacities, quantile)) for quantile in (0.0, 0.5, 0.9, 0.99, 1.0)
        ],
        "negative_run_duration_s_quantiles": [
            float(np.quantile([item["duration_s"] for item in run_stats], quantile))
            for quantile in (0.0, 0.5, 0.9, 0.99, 1.0)
        ],
        "first_twelve_negative_runs": run_stats[:12],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()

    observed_md5 = file_hash(arguments.archive, "md5")
    observed_sha256 = file_hash(arguments.archive, "sha256")
    if observed_md5 != EXPECTED_MD5 or observed_sha256 != EXPECTED_SHA256:
        raise SystemExit(
            f"Aurora archive identity mismatch: md5={observed_md5}, sha256={observed_sha256}"
        )

    metadata_results: list[dict[str, Any]] = []
    row_results: list[dict[str, Any]] = []
    first_schema: str | None = None
    with zipfile.ZipFile(arguments.archive) as archive:
        for cell_id in LFPS:
            prefix = f"empa__{cell_id}/empa__{cell_id}"
            metadata_results.append(
                metadata_audit(archive.read(f"{prefix}.metadata.json"), cell_id)
            )
            parquet_bytes = archive.read(f"{prefix}.bdf.parquet")
            row_result = row_audit(parquet_bytes, cell_id, first_schema)
            if first_schema is None:
                first_schema = str(row_result["schema"])
            row_results.append(row_result)

    protocol_counts = Counter(
        json.dumps(result["procedure_tasks"], sort_keys=True, separators=(",", ":"))
        for result in metadata_results
    )
    result = {
        "archive": {"md5": observed_md5, "sha256": observed_sha256},
        "lfp_cell_count": len(LFPS),
        "metadata_protocol_signature_count": len(protocol_counts),
        "metadata_protocol_signature_counts": sorted(protocol_counts.values()),
        "metadata_cells": metadata_results,
        "row_audits": row_results,
        "interpretation": (
            "Capacity values are trapezoidal integrations over contiguous negative-current runs. "
            "They remain candidate discharge events unless they align with each cell's protocol "
            "metadata and lower-voltage cutoff."
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Audited {len(LFPS)} LFP protocols and BDF traces; wrote {arguments.output}")


if __name__ == "__main__":
    main()
