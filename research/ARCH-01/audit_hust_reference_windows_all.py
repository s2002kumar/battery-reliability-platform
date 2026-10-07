"""Audit HUST cycle-label keys and early-capacity windows across all 77 members."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import zipfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd
from inspect_hust_archive import expected_members
from inspect_hust_payloads import EXPECTED_SHA256, RestrictedUnpickler, scalar, sha256_file


def mapping_items(value: Any) -> list[tuple[Any, Any]]:
    """Return ordered items from a pandas Series or mapping label field."""
    if isinstance(value, pd.Series):
        return list(value.items())
    if isinstance(value, Mapping):
        return list(value.items())
    raise TypeError(f"Expected cycle-keyed labels, got {type(value).__name__}")


def summarize_member(member_name: str, payload: Any) -> dict[str, Any]:
    """Validate payload labels and summarize early window sensitivity."""
    if not isinstance(payload, Mapping) or len(payload) != 1:
        raise ValueError(f"Unexpected top-level payload in {member_name}")
    cell_key, cell = next(iter(payload.items()))
    if not isinstance(cell, Mapping):
        raise ValueError(f"Unexpected cell object in {member_name}")
    required = {"data", "dq", "rul"}
    if not required.issubset({str(key) for key in cell}):
        raise ValueError(f"Missing data/dq/rul in {member_name}")
    data = cell["data"]
    if not isinstance(data, Mapping):
        raise ValueError(f"Cycle data is not a mapping in {member_name}")
    dq_items = mapping_items(cell["dq"])
    rul_items = mapping_items(cell["rul"])
    data_keys = list(data)
    dq_keys = [key for key, _ in dq_items]
    rul_keys = [key for key, _ in rul_items]
    numeric_dq: list[float] = []
    for _, value in dq_items:
        observed = scalar(value)
        if isinstance(observed, bool) or not isinstance(observed, (int, float)):
            raise ValueError(f"Non-numeric dq label in {member_name}")
        if not math.isfinite(float(observed)):
            raise ValueError(f"Non-finite dq label in {member_name}")
        numeric_dq.append(float(observed))

    windows: dict[str, dict[str, float | int]] = {}
    for window_size in (1, 3, 5, 10, 30):
        values = numeric_dq[:window_size]
        median_value = statistics.median(values)
        windows[str(window_size)] = {
            "count": len(values),
            "median_mAh": median_value,
            "range_mAh": max(values) - min(values),
            "range_percent_of_median": (
                100.0 * (max(values) - min(values)) / median_value if median_value else 0.0
            ),
            "first_vs_median_percent": (
                100.0 * (values[0] - median_value) / median_value if median_value else 0.0
            ),
        }

    return {
        "member": member_name,
        "payload_cell_key": scalar(cell_key),
        "payload_key_matches_filename": member_name.removeprefix("our_data/").removesuffix(".pkl")
        == str(scalar(cell_key)),
        "cycle_frame_count": len(data_keys),
        "dq_label_count": len(dq_items),
        "rul_label_count": len(rul_items),
        "cycle_key_bounds": [scalar(data_keys[0]), scalar(data_keys[-1])] if data_keys else [],
        "dq_key_bounds": [scalar(dq_keys[0]), scalar(dq_keys[-1])] if dq_keys else [],
        "rul_key_bounds": [scalar(rul_keys[0]), scalar(rul_keys[-1])] if rul_keys else [],
        "data_dq_key_sets_match": set(data_keys) == set(dq_keys),
        "data_rul_key_sets_match": set(data_keys) == set(rul_keys),
        "data_dq_key_order_matches": data_keys == dq_keys,
        "data_rul_key_order_matches": data_keys == rul_keys,
        "first_cycle_key": scalar(data_keys[0]) if data_keys else None,
        "dq_keys_monotonic_insertion_order": all(
            float(right) > float(left) for left, right in zip(dq_keys, dq_keys[1:], strict=False)
        ),
        "dq_first_windows": windows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()

    observed_sha256 = sha256_file(arguments.archive)
    if observed_sha256 != EXPECTED_SHA256:
        raise SystemExit(f"HUST archive SHA-256 mismatch: {observed_sha256}")

    expected = expected_members()
    payloads: list[dict[str, Any]] = []
    with zipfile.ZipFile(arguments.archive) as archive:
        actual = {item.filename for item in archive.infolist() if not item.is_dir()}
        if actual != expected:
            raise SystemExit(
                "HUST member mismatch: "
                f"missing={sorted(expected - actual)}, "
                f"extra={sorted(actual - expected)}"
            )
        for member_name in sorted(expected):
            with archive.open(member_name) as member:
                payload = RestrictedUnpickler(member).load()
            payloads.append(summarize_member(member_name, payload))

    aggregate: dict[str, Any] = {}
    for window_size in (3, 5, 10, 30):
        deviation = [
            float(item["dq_first_windows"][str(window_size)]["first_vs_median_percent"])
            for item in payloads
        ]
        range_percent = [
            float(item["dq_first_windows"][str(window_size)]["range_percent_of_median"])
            for item in payloads
        ]
        aggregate[str(window_size)] = {
            "cell_count": len(payloads),
            "first_cycle_vs_window_median_percent": {
                "min": min(deviation),
                "median": statistics.median(deviation),
                "max": max(deviation),
            },
            "within_window_range_percent_of_median": {
                "min": min(range_percent),
                "median": statistics.median(range_percent),
                "max": max(range_percent),
            },
        }

    result = {
        "archive_sha256": observed_sha256,
        "archive_bytes": arguments.archive.stat().st_size,
        "member_count": len(payloads),
        "all_payload_keys_match_member_names": all(
            item["payload_key_matches_filename"] for item in payloads
        ),
        "all_data_dq_key_sets_match": all(item["data_dq_key_sets_match"] for item in payloads),
        "all_data_rul_key_sets_match": all(item["data_rul_key_sets_match"] for item in payloads),
        "all_data_dq_key_orders_match": all(item["data_dq_key_order_matches"] for item in payloads),
        "all_data_rul_key_orders_match": all(
            item["data_rul_key_order_matches"] for item in payloads
        ),
        "all_first_cycle_keys_are_one": all(item["first_cycle_key"] == 1 for item in payloads),
        "all_dq_keys_monotonic": all(
            item["dq_keys_monotonic_insertion_order"] for item in payloads
        ),
        "early_window_aggregates": aggregate,
        "members": payloads,
        "interpretation": (
            "This audit checks label/map key coverage and early-window sensitivity across all "
            "members. It does not inspect every DataFrame row or establish that an early window is "
            "a source-declared formation test."
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Inspected early dq labels for {len(payloads)} HUST payloads; wrote {arguments.output}")


if __name__ == "__main__":
    main()
