#!/usr/bin/env python3
"""
Summarize a git diff's size and churn so a reviewer can calibrate how deep
to go before reading a single line of the actual code changes.

Usage:
    git diff --staged --numstat | python3 diff_stats.py
    git diff main...HEAD --numstat | python3 diff_stats.py
    git diff --numstat | python3 diff_stats.py --json

Reads `git diff --numstat` output from stdin (tab-separated: insertions,
deletions, path — or "-\t-\tpath" for binary files) rather than parsing a
full unified diff, since numstat is a stable, easy-to-parse format git
already produces.
"""

import argparse
import json
import sys

LARGE_TOTAL_LINES = 400
LARGE_FILE_COUNT = 15
LARGE_SINGLE_FILE_LINES = 300


def parse_numstat(lines: list[str]) -> list[dict]:
    files = []
    for line in lines:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        ins_raw, del_raw, path = parts
        binary = ins_raw == "-" or del_raw == "-"
        insertions = 0 if binary else int(ins_raw)
        deletions = 0 if binary else int(del_raw)
        files.append({
            "path": path,
            "insertions": insertions,
            "deletions": deletions,
            "total": insertions + deletions,
            "binary": binary,
        })
    return files


def summarize(files: list[dict]) -> dict:
    total_insertions = sum(f["insertions"] for f in files)
    total_deletions = sum(f["deletions"] for f in files)
    total_lines = total_insertions + total_deletions
    file_count = len(files)

    by_churn = sorted(files, key=lambda f: f["total"], reverse=True)
    largest = by_churn[0] if by_churn else None

    flags = []
    if total_lines > LARGE_TOTAL_LINES:
        flags.append(
            f"Total change is {total_lines} lines, above the {LARGE_TOTAL_LINES}-line "
            "guideline for a single focused review pass."
        )
    if file_count > LARGE_FILE_COUNT:
        flags.append(
            f"{file_count} files touched, above the {LARGE_FILE_COUNT}-file guideline — "
            "the diff may be mixing multiple unrelated concerns."
        )
    if largest and largest["total"] > LARGE_SINGLE_FILE_LINES and not largest["binary"]:
        flags.append(
            f"{largest['path']} alone has {largest['total']} changed lines — "
            "worth checking whether it should be reviewed (or split) on its own."
        )

    return {
        "file_count": file_count,
        "total_insertions": total_insertions,
        "total_deletions": total_deletions,
        "total_lines": total_lines,
        "files_by_churn": by_churn,
        "is_large": bool(flags),
        "flags": flags,
    }


def format_text(summary: dict) -> str:
    lines = [
        f"Files changed: {summary['file_count']}",
        f"Lines: +{summary['total_insertions']} / -{summary['total_deletions']} "
        f"({summary['total_lines']} total)",
    ]
    if summary["files_by_churn"]:
        lines.append("")
        lines.append("By churn (largest first):")
        for f in summary["files_by_churn"][:10]:
            marker = "(binary)" if f["binary"] else f"+{f['insertions']}/-{f['deletions']}"
            lines.append(f"  {f['path']:<50} {marker}")
        if len(summary["files_by_churn"]) > 10:
            lines.append(f"  ... and {len(summary['files_by_churn']) - 10} more")

    if summary["is_large"]:
        lines.append("")
        lines.append("Guidance:")
        for flag in summary["flags"]:
            lines.append(f"  - {flag}")
    else:
        lines.append("")
        lines.append("Guidance: diff is small enough for a normal line-by-line review pass.")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of text")
    args = parser.parse_args()

    lines = sys.stdin.readlines()
    if not lines:
        print("No diff input received on stdin (nothing changed?).", file=sys.stderr)
        sys.exit(1)

    files = parse_numstat(lines)
    summary = summarize(files)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_text(summary))


if __name__ == "__main__":
    main()
