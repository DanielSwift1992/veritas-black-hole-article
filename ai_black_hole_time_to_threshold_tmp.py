"""ai_black_hole_time_to_threshold.py
A simple script to calculate the time (in years) until an
informational singularity is reached, based on a few growth scenarios.

The core formula is:
t = ln(N_max / N0) / ln(r)

where:
- N0: Current data volume (2025)
- N_max: Bekenstein Bound for a given physical system
- r: Annual growth rate multiplier
"""

import math
# from pathlib import Path  # Раскомментируйте, если нужен CSV

# Константы
N0 = 1.448e24            # исходный объём данных, бит (2025 г.)
N_threshold = 1.74e64     # порог для ~1 мм BH, бит
start_year = 2025

# Сценарии: (человекочитаемое имя, годовой мультипликатор r = 1 + CAGR)
phi = (1 + 5 ** 0.5) / 2
scenarios = [
    ("Глобальный тренд 23 %/год", 1.23),
    ("Средний 25 %/год",          1.25),
    ("AI-ускоренный 30 %/год",    1.30),
    ("Big Data 40 %/год",         1.40),
    ("Фибоначчи φ ≈ 61.8 %/год",  phi),
]

# Заголовок для возможного CSV
print(f"{'Сценарий':35} |  r  |   t, лет | Год достижения")
print("-" * 70)

ln_ratio = math.log(N_threshold / N0)
# lines = ["scenario,r,t_years,calendar_year"]  # Для CSV

for name, r in scenarios:
    if r <= 1:
        t = float("inf")
    else:
        t = ln_ratio / math.log(r)
    year = start_year + t if math.isfinite(t) else float("inf")
    print(f"{name:35} | {r:4.3f} | {t:8.1f} | {year:10.0f}")
    # lines.append(f"{name};{r:.6g};{t:.2f};{year:.0f}")

# Path("results_time.csv").write_text("\n".join(lines), encoding="utf-8")
# print("CSV сохранён: results_time.csv")

# --- New: monetary illustration -------------------------------------------------
print("\nMonetary Illustration (USD, July 2025 prices)")

k = 1.380649e-23  # Boltzmann, J/K
T = 300           # room temperature, K
ln2 = math.log(2)
energy_per_erase = k * T * ln2  # Joule per bit erase

# Energy price
usd_per_kwh = 0.15
usd_per_joule = usd_per_kwh / (3.6e6)

cost_per_erase_usd = energy_per_erase * usd_per_joule
print(f"Landauer cost to erase 1 bit: {cost_per_erase_usd:.2e} USD")

# Rough current storage CAPEX per bit (20 TB HDD ≈ $300)
cost_storage_capex = 300 / (20e12 * 8)
print(f"Current CAPEX to buy 1 bit of HDD storage: {cost_storage_capex:.2e} USD")

# Cost to erase ALL bits at N_max
print("\nCost to erase N_max bits at Landauer limit vs φ-scenario storage need:")

cost_erase_total_usd = N_threshold * cost_per_erase_usd
print(f"• Erasing N_max bits once costs ≈ {cost_erase_total_usd:.2e} USD in irreducible energy")

# Compare with CAPEX to buy enough HDD today (overestimate)
capex_store_total_usd = N_threshold * cost_storage_capex
print(f"• Buying HDD capacity for N_max bits TODAY would cost ≈ {capex_store_total_usd:.2e} USD")

print("Note: storage price trends downward, erase cost is Physical constant → bias to ‘keep’.") 