#!/usr/bin/env python3
"""
check_dataset_sizes.py - verify that the files/directories in a folder have the
expected (compressed) size according to a reference table.

The reference values are rounded UP, so the measured size is rounded up to the
same precision as the expected value and compared for equality. Example: with an
expected value of "1.4", a measured 1.32 GB rounds to 1.4 and passes, while a
measured 1.41 GB rounds to 1.5 and fails.

Typical usage:
    python3 check_dataset_sizes.py                       # uses DEFAULT_DIRECTORY
    python3 check_dataset_sizes.py /path/to/datasets
    python3 check_dataset_sizes.py /path/to/datasets --mode tolerance --tol 0.10

Exit codes: 0 = every dataset is correct, 1 = something is wrong or missing,
2 = usage error.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_CEILING

# --------------------------------------------------------------------------
# Directory checked when no path is given on the command line. Edit this to
# point at your own dataset folder.
# --------------------------------------------------------------------------
DEFAULT_DIRECTORY = "/mnt/beegfs/sranieri/PIDSMaker/data"

# --------------------------------------------------------------------------
# Reference table (COMPRESSED size in GB, rounded up).
# Values are strings so their precision can be derived:
# "1.4" -> compared to a tenth of a GB; "36" -> compared to a whole GB.
# --------------------------------------------------------------------------
EXPECTED_GB: dict[str, str] = {
    "CADETS_E3":         "1.4",
    "THEIA_E3":          "1.1",
    "CLEARSCOPE_E3":     "0.6",
    "FIVEDIRECTIONS_E3": "3.2",
    "TRACE_E3":          "11",
    "CADETS_E5":         "36",
    "THEIA_E5":          "5.8",
    "CLEARSCOPE_E5":     "6.2",
    "FIVEDIRECTIONS_E5": "39",
    "TRACE_E5":          "91",
    "OPTC_H201":         "2",
    "OPTC_H_501":        "1.5",
    "OPTC_H051":         "1.7",
    "ATLASV2_EDR":       "0.2",
    "CARBANAKV2_EDR":    "1.1",
}

UNITS = {"gb": Decimal(10) ** 9, "gib": Decimal(2) ** 30}

ARCHIVE_SUFFIXES = (
    ".tar.gz", ".tar.bz2", ".tar.xz", ".tar.zst",
    ".tgz", ".tbz2", ".txz",
    ".gz", ".bz2", ".xz", ".zst", ".zip", ".7z", ".rar", ".tar",
    ".json", ".bin", ".csv", ".log", ".txt", ".parquet", ".dump"
)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def normalize(name: str) -> str:
    """CADETS_E3 / cadets-e3.tar.gz / OPTC_H_501 -> CADETSE3 / OPTCH501."""
    n = name.strip()
    changed = True
    while changed:                      # strip stacked extensions (e.g., .tar.gz)
        changed = False
        low = n.lower()
        for suf in ARCHIVE_SUFFIXES:
            if low.endswith(suf):
                n = n[: -len(suf)]
                changed = True
                break
    return re.sub(r"[^A-Za-z0-9]", "", n).upper()


def decimals_of(value_str: str) -> int:
    return len(value_str.split(".")[1]) if "." in value_str else 0


def ceil_to(value: Decimal, decimals: int) -> Decimal:
    """Round up to the given number of decimal places."""
    return value.quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_CEILING)


def dir_size(path: str) -> int:
    """Recursively sum file sizes, ignoring symbolic links."""
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                if os.path.islink(fp):
                    continue
                total += os.stat(fp).st_size
            except OSError:
                pass
    return total


def entry_size(path: str) -> int:
    if os.path.isdir(path):
        return dir_size(path)
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------
def measure(directory: str, dataset: str) -> int | None:
    """Total size in bytes of the entries matching a dataset, or None if absent."""
    key = normalize(dataset)
    matched = []
    for entry in sorted(os.listdir(directory)):
        norm = normalize(entry)
        # exact name match, or multi-part archive (CADETS_E3.part1.gz, ...)
        if norm == key or norm.startswith(key):
            matched.append(entry)
    if not matched:
        return None
    return sum(entry_size(os.path.join(directory, m)) for m in matched)


def is_correct(measured: Decimal, exp_str: str, mode: str, tol: float) -> bool:
    exp_dec = Decimal(exp_str)
    if mode == "ceil":
        return ceil_to(measured, decimals_of(exp_str)) == exp_dec
    return abs(measured - exp_dec) <= Decimal(str(tol)) * exp_dec


# --------------------------------------------------------------------------
def main() -> int:
    p = argparse.ArgumentParser(
        description="Verify the compressed size of datasets in a directory.")
    p.add_argument("--directory", default=DEFAULT_DIRECTORY,
                   help=f"directory to check (default: {DEFAULT_DIRECTORY})")
    p.add_argument("--mode", choices=["ceil", "tolerance"], default="ceil",
                   help="ceil (default): round the measured size up and require an "
                        "exact match; tolerance: compare with a relative margin")
    p.add_argument("--tol", type=float, default=0.10,
                   help="relative tolerance for --mode tolerance (default: 0.10 = 10%%)")
    p.add_argument("--unit", choices=["gb", "gib"], default="gb",
                   help="GB=10^9 bytes (default), GiB=2^30")
    args = p.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory.", file=sys.stderr)
        if args.directory == DEFAULT_DIRECTORY:
            print("Pass a path on the command line or edit DEFAULT_DIRECTORY "
                  "at the top of this script.", file=sys.stderr)
        return 2

    directory = os.path.abspath(args.directory)
    label = "GiB" if args.unit == "gib" else "GB"
    width = max(len(name) for name in EXPECTED_GB)
    ok_mark, bad_mark = "OK", "X"
    if (sys.stdout.encoding or "").lower().startswith("utf"):
        ok_mark, bad_mark = "\u2713", "\u2717"

    print(f"Directory: {directory}\n")
    print(f"{'DATASET':<{width}}  {'EXPECTED':>11}  {'MEASURED':>12}   CHECK")
    print("-" * (width + 36))

    correct = 0
    for dataset, exp_str in EXPECTED_GB.items():
        total = measure(directory, dataset)
        if total is None:
            print(f"{dataset:<{width}}  {float(exp_str):>8.2f} {label:<2}  "
                  f"{'not found':>12}   {bad_mark}")
            continue
        measured = Decimal(total) / UNITS[args.unit]
        good = is_correct(measured, exp_str, args.mode, args.tol)
        correct += good
        print(f"{dataset:<{width}}  {float(exp_str):>8.2f} {label:<2}  "
              f"{float(measured):>9.3f} {label:<2}   {ok_mark if good else bad_mark}")

    print("-" * (width + 36))
    print(f"{correct}/{len(EXPECTED_GB)} datasets match the expected size.")
    return 0 if correct == len(EXPECTED_GB) else 1


if __name__ == "__main__":
    sys.exit(main())