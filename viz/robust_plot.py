import math
import matplotlib.pyplot as plt
try:
    from .style import init_matplotlib, apply_axes_style, save_figure  # type: ignore
except Exception:
    from style import init_matplotlib, apply_axes_style, save_figure  # type: ignore
from pathlib import Path
import os

N0 = 1.448e24
N_MAX = 1.74e64
START_YEAR = 2025
phi = (1 + 5 ** 0.5) / 2

factor = 2  # Doppler recalibration

# Compute times
base_years = math.log(N_MAX / N0) / math.log(phi)
recal_years = math.log((N_MAX * factor) / N0) / math.log(phi)

# Timeline axis
years = list(range(0, int(recal_years) + 20))
N_base = [N0 * (phi ** t) for t in years]

init_matplotlib()
fig = plt.figure(figsize=(6,4))
plt.yscale('log')
plt.plot([START_YEAR + y for y in years], N_base, label='Data growth (φ)')
plt.axhline(N_MAX, color='red', linestyle='--', label='Original Bekenstein bound')
plt.axhline(N_MAX * factor, color='orange', linestyle=':', label='Rescaled bound ×2')
plt.xlabel('Calendar year')
plt.ylabel('Bits stored')
plt.title('Robustness to distance rescaling')
plt.legend()
apply_axes_style(plt.gca())
art_dir = os.getenv('BH_ARTIFACT_DIR', 'build/artifacts')
os.makedirs(art_dir, exist_ok=True)
output = Path(art_dir) / 'robust_recal.png'
save_figure(fig, str(output))
print(f'Saved {output}')