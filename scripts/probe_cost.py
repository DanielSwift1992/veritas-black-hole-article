"""Estimate energy and monetary cost of sending a simple probe ("courier") to a target star.
Outputs a small CSV for easy inclusion in the article.
"""

import argparse
import csv
import math
import sys

C = 299_792_458  # m/s
USD_PER_KWH = 0.1  # optimistic future solar cost
USD_PER_J = USD_PER_KWH / 3_600_000  # 1 kWh = 3.6e6 J

DEFAULTS = dict(
    distance_m=4.0e16,   # ~4.2 ly
    mass_kg=1.0,         # 1 kg probe
    velocity_frac_c=0.1, # 0.1c
    payload_bits=8e12,   # 1 TB
)

# Earth annual solar energy (cross-section): πR² S₀ × year
R_EARTH = 6.371e6  # m
SOLAR_CONST = 1361  # W/m²
SECONDS_YEAR = 3.15576e7
E_SUN_YEAR = math.pi * R_EARTH**2 * SOLAR_CONST * SECONDS_YEAR  # J ≈ 6.2e24


def calc(args):
    v = args.vfrac * C
    E_k = 0.5 * args.mass * v * v  # J
    cost_energy = E_k * USD_PER_J      # USD
    cost_per_bit = cost_energy / args.payload
    return E_k, cost_energy, cost_per_bit


def main():
    p = argparse.ArgumentParser(description="Courier probe cost model")
    p.add_argument("--distance", type=float, default=DEFAULTS["distance_m"], help="distance to target (meters)")
    p.add_argument("--mass", type=float, default=DEFAULTS["mass_kg"], help="probe mass (kg)")
    p.add_argument("--vfrac", type=float, default=DEFAULTS["velocity_frac_c"], help="cruise speed as fraction of c")
    p.add_argument("--payload", type=float, default=DEFAULTS["payload_bits"], help="payload size (bits)")
    p.add_argument("--csv", action="store_true")
    args = p.parse_args()

    E_k, cost_usd, cost_per_bit = calc(args)
    E_per_bit = E_k / args.payload
    ratio_Esun = E_k / E_SUN_YEAR
    ratio_Esun_bit = E_per_bit / E_SUN_YEAR
    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(["distance_m","mass_kg","v_frac_c","payload_bits","E_k_J","Cost_USD","Cost_USD_per_bit"])
        writer.writerow([args.distance,args.mass,args.vfrac,args.payload,f"{E_k:.3e}",f"{cost_usd:.3e}",f"{cost_per_bit:.3e}",f"{E_per_bit:.3e}",f"{ratio_Esun:.3e}",f"{ratio_Esun_bit:.3e}"])
    else:
        print(f"Kinetic energy: {E_k:.3e} J ({ratio_Esun:.2e} of Earth-year insolation)")
        print(f"Energy per bit: {E_per_bit:.3e} J ({ratio_Esun_bit:.2e} of annual insolation)")
        print(f"Energy cost (@{USD_PER_KWH} USD/kWh): {cost_usd:.3e} USD")
        print(f"Cost per bit for payload of {args.payload:.1e} bits: {cost_per_bit:.3e} USD/bit")

if __name__ == "__main__":
    main()