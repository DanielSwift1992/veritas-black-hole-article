import numpy as np
import matplotlib.pyplot as plt
import math

# Data
N0 = 1.448e24
N_max = 1.74e64
start_year = 2025
phi = (1 + 5**0.5) / 2

scenarios = {
    "23% CAGR": 1.23,
    "40% CAGR": 1.40,
    "φ-growth": phi,
}

# Plot setup
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data
for name, r in scenarios.items():
    t = np.log(N_max / N0) / np.log(r)
    years = np.linspace(0, t, 100)
    N = N0 * (r**years)
    ax.plot(start_year + years, N, label=f"{name} (r={r:.2f})")

# Formatting
ax.axhline(N_max, color='red', linestyle='--', label='Bekenstein Bound (N_max)')
ax.set_yscale('log')
ax.set_xlabel('Year')
ax.set_ylabel('Global Data (bits, log scale)')
ax.set_title('Informational Singularity: A ~190-Year Timeline')
ax.legend()
ax.grid(True, which="both", ls="-", color='0.2')

# Save with transparent background
plt.savefig('growth_curves.png', transparent=True)
print("Plot saved to growth_curves.png") 