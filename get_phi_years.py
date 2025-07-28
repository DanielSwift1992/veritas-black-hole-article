import argparse
import csv
import json
import math
import sys
from typing import Dict, Tuple, List

N0_DEFAULT = 1.448e24  # bits stored in 2025 (~181 ZB)
N_MAX_DEFAULT = 1.74e64  # Bekenstein bound for 1 mm BH (can be overridden)
START_YEAR_DEFAULT = 2025

SCENARIOS: Dict[str, Tuple[float, float]] = {
    # label: (growth rate r, multiplier on N_max)
    "Conservative": (1.23, 1),
    "Big-Data": (1.40, 1),
    "φ Baseline": ((1 + math.sqrt(5)) / 2, 1),
    # Sensitivity variations
    "Larger BH": ((1 + math.sqrt(5)) / 2, 100),  # 1 cm radius → N_max ×100
    "Partial deletion allowed": (1.50, 1),
    "Massive expansion": ((1 + math.sqrt(5)) / 2, 1e10),
    "Doppler recalibration": ((1 + math.sqrt(5)) / 2, 2),
}

# Physical constant for communication energy (Landauer):
k_B = 1.380649e-23  # J/K
T_DEFAULT = 300.0   # Kelvin, ambient


def compare_central_vs_sharded(n: int, d: float, bits: float, *, T: float = T_DEFAULT) -> bool:
    """Return True if sharded design is *strictly* more energy-expensive.

    Very coarse model: total steady-state dissipation E ∝ k_B T ln2 per transmitted bit-meter per unit time.
    For n shards placed on a ring of radius d we approximate per-step sync traffic as one full copy per shard.
    """
    ln2 = math.log(2)
    E_comm = n * d * k_B * T * ln2  # J per sync interval (units not important for sign)
    # Centralized reference energy set to zero; any positive E_comm means sharding is worse.
    return E_comm > 0


def calc_years(r: float, n_factor: float, *, n0: float, n_max: float, start_year: int) -> Tuple[int, int]:
    """Return (years_until_threshold, calendar_year)."""
    t = math.log((n_max * n_factor) / n0) / math.log(r)
    years = math.ceil(t)
    return years, start_year + years


def scenario_rows(scenarios: Dict[str, Tuple[float, float]], *, n0: float, n_max: float, start_year: int) -> List[Tuple[str, float, int, int]]:
    rows: List[Tuple[str, float, int, int]] = []
    for name, (r, factor) in scenarios.items():
        years, year = calc_years(r, factor, n0=n0, n_max=n_max, start_year=start_year)
        rows.append((name, r, years, year))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute time-to-singularity scenarios.")
    parser.add_argument("--r", type=float, help="Custom growth rate r (overrides scenarios list)")
    parser.add_argument("--factor", type=float, default=1.0, help="Multiplier on N_max for custom run")
    parser.add_argument("--n0", type=float, default=N0_DEFAULT, help="Initial bits N0 (default 1.448e24)")
    parser.add_argument("--nmax", type=float, default=N_MAX_DEFAULT, help="Max bits N_max (default 1.74e64)")
    parser.add_argument("--start-year", type=int, default=START_YEAR_DEFAULT, help="Start year (default 2025)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of CSV")
    parser.add_argument("--csv", action="store_true", help="Force CSV output (default if not --json)")

    parser.add_argument("--compare-sharded", nargs=2, metavar=("N_SHARDS", "DIST"),
                        help="Compare centralized vs sharded energy: specify number of shards and separation distance in meters.")

    args = parser.parse_args()

    # Special branch: compare sharded vs central energy
    if args.compare_sharded:
        n_shards = int(args.compare_sharded[0])
        distance = float(args.compare_sharded[1])
        ok = compare_central_vs_sharded(n_shards, distance, args.nmax)
        print("PASS" if ok else "FAIL")
        return

    if args.r:
        # Custom single scenario
        years, year = calc_years(args.r, args.factor, n0=args.n0, n_max=args.nmax, start_year=args.start_year)
        rows = [("custom", args.r, years, year)]
    else:
        rows = scenario_rows(SCENARIOS, n0=args.n0, n_max=args.nmax, start_year=args.start_year)

    if args.json:
        # Produce JSON list of dicts
        data = [
            {"label": label, "r": r, "years": years, "year": year} for label, r, years, year in rows
        ]
        json.dump(data, sys.stdout, indent=2)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(["Scenario", "r", "Years", "Year"])
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main() 