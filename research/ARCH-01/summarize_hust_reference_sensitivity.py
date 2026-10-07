"""Summarize candidate early-cycle HUST reference windows from audit outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


def load_audit(path: Path) -> dict[str, Any]:
    """Load one JSON output emitted by the restricted HUST payload inspector."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("members"), dict):
        raise ValueError(f"Invalid HUST audit JSON: {path}")
    return value


def sha256_file(path: Path) -> str:
    """Hash an input JSON file with bounded memory use."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("audits", nargs="+", type=Path)
    arguments = parser.parse_args()

    cells: list[dict[str, Any]] = []
    inputs: list[dict[str, str]] = []
    for path in arguments.audits:
        audit = load_audit(path)
        inputs.append({"path": path.as_posix(), "sha256": sha256_file(path)})
        for member_name, summary in audit["members"].items():
            dq = summary["dq"]
            windows = dq.get("early_window_statistics", {})
            if not {"1", "3", "5", "10", "30"}.issubset(windows):
                raise ValueError(f"Missing early-window statistics for {member_name}")
            cells.append(
                {
                    "member": member_name,
                    "cycle_count": dq["length"],
                    "first_valid_cycle_key": dq["first_key"],
                    "last_cycle_key": dq["last_key"],
                    "dq_match_count": summary["dq_vs_peak_minus_final_capacity"][
                        "matched_cycle_count"
                    ],
                    "max_dq_relation_error_mAh": summary["dq_vs_peak_minus_final_capacity"][
                        "max_absolute_difference_mAh"
                    ],
                    "window_comparison": {
                        window: {
                            "first_vs_window_median_percent": windows[window][
                                "first_vs_median_percent"
                            ],
                            "window_range_percent_of_median": (
                                100.0 * windows[window]["range"] / windows[window]["median"]
                                if windows[window]["median"] != 0
                                else None
                            ),
                        }
                        for window in ("3", "5", "10", "30")
                    },
                }
            )

    if not cells:
        raise ValueError("No cell payload summaries were supplied")

    aggregate: dict[str, Any] = {}
    for window in ("3", "5", "10", "30"):
        first_differences = [
            float(cell["window_comparison"][window]["first_vs_window_median_percent"])
            for cell in cells
        ]
        ranges = [
            float(cell["window_comparison"][window]["window_range_percent_of_median"])
            for cell in cells
        ]
        aggregate[window] = {
            "cell_count": len(cells),
            "first_vs_window_median_percent": {
                "min": min(first_differences),
                "median": statistics.median(first_differences),
                "max": max(first_differences),
            },
            "window_range_percent_of_median": {"min": min(ranges), "max": max(ranges)},
        }

    result = {
        "audit_member_count": len(cells),
        "audited_cycle_count": sum(cell["cycle_count"] for cell in cells),
        "audited_row_count": sum(
            summary["data"]["total_rows"]
            for path in arguments.audits
            for summary in load_audit(path)["members"].values()
        ),
        "inputs": inputs,
        "window_aggregates": aggregate,
        "members": cells,
        "interpretation": (
            "Descriptive sensitivity only; a stable-window comparison does not establish "
            "a source-defined formation or reference-capacity rule."
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Summarized {len(cells)} HUST payloads into {arguments.output}")


if __name__ == "__main__":
    main()
