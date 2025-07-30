import numpy as np
import matplotlib.pyplot as plt
import math
import os

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

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]  # blue, orange, green

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 7), dpi=120)

# Plot data
for idx, (name, r) in enumerate(scenarios.items()):
    t = np.log(N_max / N0) / np.log(r)
    years = np.linspace(0, t, 200)
    N = N0 * (r**years)
    color = colors[idx % len(colors)]
    ax.plot(start_year + years, N, label=f"{name} (r={r:.2f})", linewidth=2.5, color=color)
    # Точка соприкосновения
    x_cross = start_year + t
    ax.scatter([x_cross], [N_max], color=color, s=80, zorder=5)
    ax.annotate(f"{int(x_cross)}",
                xy=(x_cross, N_max),
                xytext=(x_cross+5, N_max*2),
                textcoords='data',
                fontsize=12,
                color=color,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                ha='left', va='bottom',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=1, alpha=0.0))

# Formatting
ax.axhline(N_max, color='red', linestyle='--', label='Bekenstein Bound (N_max)', linewidth=2)
ax.set_yscale('log')
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Global Data (bits, log scale)', fontsize=14)
ax.set_title('Informational Singularity: Timeline to Physical Limit', fontsize=17, pad=15)
ax.legend(fontsize=13, frameon=True, loc='upper left')
ax.grid(True, which="both", ls="-", color='#e0e0e0', alpha=0.7)
fig.tight_layout()

# Save with white background
art_dir = os.getenv('BH_ARTIFACT_DIR', 'build/artifacts')
os.makedirs(art_dir, exist_ok=True)
out_png = os.path.join(art_dir, 'growth_curves.png')
plt.savefig(out_png, transparent=False, bbox_inches='tight')
print(f"Plot saved to {out_png}") 