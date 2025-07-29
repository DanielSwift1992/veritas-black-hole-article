"""
Compute crossover year where storing a bit becomes cheaper than deleting it under Landauer's limit.

Assumptions
-----------
* Cost to delete a bit (Landauer at 300 K): C_DELETE = 1.2 × 10⁻²⁸ USD.
* Up-front storage cost in 2025: C_STORE_2025 = 2 × 10⁻¹² USD per bit (consumer HDD scale).
* Storage cost halves every 2 years ⇒ yearly divisor √2 ≈ 1.4142.

The script prints either CSV (default) or JSON so that automated checks can compare numbers
against the table embedded in the article.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from typing import List, Dict, Any

C_DELETE = 1.2e-28  # USD per bit (constant physical cost)
C_STORE_2025 = 2e-12  # USD per bit (2025 baseline hardware)
FACTOR_YEARLY = math.sqrt(2)  # ≈ 1.414213562 – storage cost divisor per year
DEFAULT_YEARS = [2025, 2050, 2075, 2100, 2106, 2125, 2150, 2217]

BYTES_PER_GB = 1_000_000_000  # 1e9 bytes
BITS_PER_GB = BYTES_PER_GB * 8

DIST_LY_METERS = 9.46e15  # one light-year in meters approximation

BITS_PER_DELETE_LABEL = "BitsPerDelete"
TRANSMIT_RATIO_LABEL = "RatioStoreToTransmit"


def orders_mag(ratio: float) -> float:
    """Return base-10 logarithm of the ratio, can be negative."""
    return math.log10(ratio)


def storage_cost(year: int, *, start_year: int = 2025) -> float:
    """Return the up-front cost (USD) to store one bit in *year*."""
    years_since = year - start_year
    return C_STORE_2025 / (FACTOR_YEARLY ** years_since)


def compute_rows(years: List[int]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for year in years:
        cost_store = storage_cost(year)
        ratio = cost_store / C_DELETE  # < 1 => storing cheaper than deleting
        orders = orders_mag(ratio)
        bits_per_delete = 1 / ratio  # how many bits storable for cost of deleting one
        store_gb = cost_store * BITS_PER_GB
        delete_gb = C_DELETE * BITS_PER_GB
        transmit_cost = C_DELETE * DIST_LY_METERS  # simplistic linear scaling
        store_transmit_ratio = cost_store / transmit_cost
        rows.append({
            "Year": year,
            "StoreUSD_perBit": cost_store,
            "DeleteUSD_perBit": C_DELETE,
            "TransmitUSD_perBit": transmit_cost,
            "StoreUSD_perGB": store_gb,
            "DeleteUSD_perGB": delete_gb,
            "RatioStoreToDelete": ratio,
            "Log10Ratio": orders,
            BITS_PER_DELETE_LABEL: bits_per_delete,
            TRANSMIT_RATIO_LABEL: store_transmit_ratio,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute storage vs deletion cost per bit over time.")
    parser.add_argument("--csv", action="store_true", help="Output CSV (default if no --json)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of CSV")
    parser.add_argument("--start", type=int, default=2025, help="Start year (default 2025)")
    parser.add_argument("--end", type=int, default=2217, help="End year inclusive (default 2217)")
    parser.add_argument("--step", type=int, default=25, help="Year step (default 25)")
    args = parser.parse_args()

    if args.step <= 0:
        parser.error("--step must be positive")

    if (args.start, args.end, args.step) == (2025, 2217, 25):
        years = DEFAULT_YEARS
    else:
        years = list(range(args.start, args.end + 1, args.step))

    rows = compute_rows(years)

    if args.json:
        json.dump(rows, sys.stdout, indent=2)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(["Year", "StoreUSD/bit", "DeleteUSD/bit", "TransmitUSD/bit@1ly", "StoreUSD/GB", "Ratio(S/D)", "log10R(S/D)", "BitsPerDelete", "Ratio(S/T)"])
        for row in rows:
            writer.writerow([
                row["Year"],
                f"{row['StoreUSD_perBit']:.3e}",
                f"{row['DeleteUSD_perBit']:.1e}",
                f"{row['TransmitUSD_perBit']:.1e}",
                f"{row['StoreUSD_perGB']:.2e}",
                f"{row['RatioStoreToDelete']:.1e}",
                f"{row['Log10Ratio']:+.1f}",
                f"{row[BITS_PER_DELETE_LABEL]:.1e}",
                f"{row[TRANSMIT_RATIO_LABEL]:.1e}",
            ])


if __name__ == "__main__":
    main()
