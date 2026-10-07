"""Inventory HUST pickle archives without executing pickle payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import pickletools
import zipfile
from pathlib import Path
from typing import Any

EXPECTED_SHA256 = "071d24617153693b0d29059568525e620f6af6512acc9d00c98c7adcf15125db"


def expected_members() -> set[str]:
    """Return the 77 exact member paths recorded by the Mendeley archive."""
    groups = {
        1: range(1, 9),
        2: range(2, 9),
        3: range(1, 9),
        4: range(1, 9),
        5: range(1, 8),
        6: (1, 2, 3, 4, 5, 6, 8),
        7: range(1, 9),
        8: range(1, 9),
        9: range(1, 9),
        10: range(1, 9),
    }
    return {f"our_data/{group}-{cell}.pkl" for group, cells in groups.items() for cell in cells}


def archive_sha256(path: Path) -> str:
    """Hash the exact source archive without loading it into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_pickle_opcodes(data: bytes) -> dict[str, Any]:
    """Return static pickle opcode and global-reference evidence only."""
    operations = list(pickletools.genops(data))
    globals_seen: set[str] = set()
    stack_global_windows: list[dict[str, Any]] = []
    for index, (opcode, argument, position) in enumerate(operations):
        if opcode.name == "GLOBAL":
            globals_seen.add(str(argument))
        elif opcode.name == "STACK_GLOBAL":
            nearby_strings = [
                {"opcode": prior_opcode.name, "value": prior_arg}
                for prior_opcode, prior_arg, _ in operations[max(0, index - 12) : index]
                if isinstance(prior_arg, str) and len(prior_arg) < 256
            ]
            stack_global_windows.append(
                {"offset": position, "preceding_string_constants": nearby_strings}
            )
    return {
        "protocol": max(
            (int(argument) for opcode, argument, _ in operations if opcode.name == "PROTO"),
            default=0,
        ),
        "opcode_count": len(operations),
        "global_opcodes": sorted(globals_seen),
        "stack_global_windows": stack_global_windows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--expected-sha256", default=EXPECTED_SHA256, help="Expected Mendeley source checksum"
    )
    arguments = parser.parse_args()

    observed_sha256 = archive_sha256(arguments.archive)
    if observed_sha256 != arguments.expected_sha256.lower():
        raise SystemExit(
            "Archive SHA-256 mismatch: "
            f"expected {arguments.expected_sha256}, observed {observed_sha256}"
        )

    with zipfile.ZipFile(arguments.archive) as archive:
        infos = [item for item in archive.infolist() if not item.is_dir()]
        actual_members = {item.filename for item in infos}
        expected = expected_members()
        if actual_members != expected:
            missing = sorted(expected - actual_members)
            extra = sorted(actual_members - expected)
            raise SystemExit(f"Archive member mismatch: missing={missing}; extra={extra}")

        size_sorted = sorted(infos, key=lambda item: (item.file_size, item.filename))
        selected_names = {
            "our_data/1-1.pkl",
            "our_data/2-2.pkl",
            "our_data/5-7.pkl",
            "our_data/6-8.pkl",
            "our_data/10-8.pkl",
            size_sorted[0].filename,
            size_sorted[-1].filename,
        }
        sample_opcodes: dict[str, Any] = {}
        for name in sorted(selected_names):
            with archive.open(name) as member:
                sample_opcodes[name] = inspect_pickle_opcodes(member.read())

        result = {
            "archive": str(arguments.archive.resolve()),
            "archive_bytes": arguments.archive.stat().st_size,
            "archive_sha256": observed_sha256,
            "non_directory_member_count": len(infos),
            "member_inventory": [
                {
                    "name": item.filename,
                    "compressed_bytes": item.compress_size,
                    "uncompressed_bytes": item.file_size,
                    "crc32": f"{item.CRC:08x}",
                }
                for item in sorted(infos, key=lambda item: item.filename)
            ],
            "expected_inventory_match": True,
            "pickle_static_inspection": sample_opcodes,
            "deserialization_performed": False,
        }

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(infos)} members; SHA-256 {observed_sha256}; wrote {arguments.output}")


if __name__ == "__main__":
    main()
