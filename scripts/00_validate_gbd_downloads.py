#!/usr/bin/env python3
"""Validate expected GBD download files against the Phase 1 manifest.

This script avoids third-party dependencies so it can run before the full
analysis environment is provisioned.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ValidationRow:
    export_id: str
    priority: str
    status: str
    analysis_module: str
    path: str
    exists: bool
    header_ok: bool
    missing_columns: list[str]


def read_manifest(manifest_path: Path) -> list[dict[str, str]]:
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_required_columns(raw: str) -> list[str]:
    return [value.strip() for value in raw.split(";") if value.strip()]


def read_header(csv_path: Path) -> list[str]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def validate_row(project_root: Path, row: dict[str, str]) -> ValidationRow:
    rel_dir = row["target_subdir"].strip()
    filename = row["output_filename"].strip()
    full_path = project_root / rel_dir / filename
    exists = full_path.exists()
    header_ok = False
    missing_columns: list[str] = []

    if exists and full_path.suffix.lower() == ".csv":
        header = read_header(full_path)
        required = parse_required_columns(row.get("required_columns", ""))
        missing_columns = [column for column in required if column not in header]
        header_ok = not missing_columns

    return ValidationRow(
        export_id=row["export_id"],
        priority=row["priority"],
        status=row["status"],
        analysis_module=row.get("analysis_module", "").strip(),
        path=str(full_path.relative_to(project_root)),
        exists=exists,
        header_ok=header_ok if exists else False,
        missing_columns=missing_columns,
    )


def summarize_bucket(rows: Iterable[ValidationRow]) -> dict[str, int]:
    rows = list(rows)
    return {
        "total": len(rows),
        "existing": sum(1 for row in rows if row.exists),
        "missing": sum(1 for row in rows if not row.exists),
        "header_ok": sum(1 for row in rows if row.exists and row.header_ok),
        "header_bad": sum(1 for row in rows if row.exists and not row.header_ok),
    }


def summarize(rows: Iterable[ValidationRow]) -> dict[str, object]:
    rows = list(rows)
    by_priority: dict[str, dict[str, int]] = {}
    by_analysis_module: dict[str, dict[str, int]] = {}

    for key in sorted({row.priority for row in rows}):
        by_priority[key] = summarize_bucket(row for row in rows if row.priority == key)

    for key in sorted({row.analysis_module for row in rows}):
        by_analysis_module[key] = summarize_bucket(
            row for row in rows if row.analysis_module == key
        )

    summary = summarize_bucket(rows)
    summary["by_priority"] = by_priority
    summary["by_analysis_module"] = by_analysis_module
    return summary


def split_cli_values(values: list[str]) -> set[str]:
    out: set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                out.add(item)
    return out


def print_bucket_summary(title: str, rows: dict[str, dict[str, int]]) -> None:
    print(title)
    for key in sorted(rows):
        payload = rows[key]
        print(
            f"- {key}: total={payload['total']}, existing={payload['existing']}, "
            f"missing={payload['missing']}, header_ok={payload['header_ok']}, "
            f"header_bad={payload['header_bad']}"
        )
    print("")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate expected GBD download files.")
    parser.add_argument(
        "--project-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Project root containing metadata/gbd_download_manifest.csv",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional explicit path to the manifest CSV.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any required file is missing or malformed.",
    )
    parser.add_argument(
        "--analysis-module",
        action="append",
        default=[],
        help="Optional analysis_module filter. Repeat or pass comma-separated values.",
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=None,
        help="Optional explicit JSON output path. Filtered runs do not write a log unless this is set.",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    manifest_path = args.manifest or (project_root / "metadata" / "gbd_download_manifest.csv")
    selected_modules = split_cli_values(args.analysis_module)

    manifest_rows = read_manifest(manifest_path)
    if selected_modules:
        manifest_rows = [
            row for row in manifest_rows if row.get("analysis_module", "").strip() in selected_modules
        ]

    if args.log_path is not None:
        log_path = args.log_path.resolve()
    elif selected_modules:
        log_path = None
    else:
        log_path = project_root / "logs" / "gbd_download_validation_summary.json"

    rows = [validate_row(project_root, row) for row in manifest_rows]
    summary = summarize(rows)

    print("GBD download validation summary")
    print(
        json.dumps(
            {
                "total": summary["total"],
                "existing": summary["existing"],
                "missing": summary["missing"],
                "header_ok": summary["header_ok"],
                "header_bad": summary["header_bad"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    print("")
    print_bucket_summary("Priority summary", summary["by_priority"])
    print_bucket_summary("Analysis module summary", summary["by_analysis_module"])

    for row in rows:
        state = "OK" if row.exists and row.header_ok else ("MISSING" if not row.exists else "HEADER_BAD")
        print(f"[{state}] {row.export_id} ({row.analysis_module}) -> {row.path}")
        if row.missing_columns:
            print(f"  missing columns: {', '.join(row.missing_columns)}")

    payload = {
        "summary": summary,
        "rows": [
            {
                "export_id": row.export_id,
                "priority": row.priority,
                "status": row.status,
                "analysis_module": row.analysis_module,
                "path": row.path,
                "exists": row.exists,
                "header_ok": row.header_ok,
                "missing_columns": row.missing_columns,
            }
            for row in rows
        ],
    }
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.strict:
        required_failures = [
            row
            for row in rows
            if row.priority in {"baseline", "required"} and (not row.exists or not row.header_ok)
        ]
        if required_failures:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
