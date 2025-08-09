import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from pathlib import Path
import os
try:
    from .style import init_matplotlib, save_figure  # type: ignore
except Exception:
    from style import init_matplotlib, save_figure  # type: ignore

init_matplotlib()
fig, ax = plt.subplots(figsize=(12,6.2))
ax.set_aspect('equal')
ax.axis('off')

# Parameters
R = 1.0  # radius of centralized droplet (right)
n = 9    # number of shards (left), factor sqrt(n) increase in total perimeter

# Left: sharded depiction with n equal small circles of radius r = R/sqrt(n)
r = R / math.sqrt(n)
cols = int(math.sqrt(n))
rows = int(math.ceil(n / cols))
spacing = 2.25 * r
start_x = -2.55
start_y = 0.6 if rows > 1 else -0.05

# Number of small circles whose total perimeter equals the centralized perimeter: k ≈ sqrt(n)
k = int(round(math.sqrt(n)))

count = 0
for i in range(rows):
    for j in range(cols):
        if count >= n:
            break
        x = start_x + j * spacing
        y = start_y - i * spacing
        color = '#ff7f0e' if count < k else '#1f77b4'  # orange equals central surface, blue is excess
        face = (1.0, 0.5, 0.0, 0.08) if count < k else (0.12, 0.47, 0.71, 0.08)
        ax.add_patch(Circle((x,y), r, edgecolor=color, facecolor=face, linewidth=3.0))
        count += 1

root_n = math.sqrt(n)
central_perim = 2 * math.pi * R

# Right: centralized (thicker line)
ax.add_patch(Circle((2.15,-0.1), R, edgecolor='#ff7f0e', facecolor=(1.0, 0.5, 0.0, 0.08), linewidth=3.0))  # slight vertical/horizontal centering

# No legend/text in figure; keep clean for MD captions

plt.xlim(-3.0,3.8)
plt.ylim(-1.75,1.55)

# Minimal legend (color meaning) and concise note about equal area
legend_elements = [
    Line2D([0],[0], color='#ff7f0e', lw=3.0, label='Orange: sum perimeter = 2πR'),
    Line2D([0],[0], color='#1f77b4', lw=3.0, label='Blue: excess perimeter'),
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=11)

# Optional ultra-brief caption inside figure (kept one line to avoid overflow)
note = 'Equal area: n·πr² = πR². Perimeter grows to 2πR·√n.'
ax.text(0.0, -1.6, note, ha='center', va='top', fontsize=12)
plt.tight_layout()
art_dir = os.getenv('BH_ARTIFACT_DIR', 'build/artifacts')
os.makedirs(art_dir, exist_ok=True)
output = Path(art_dir) / 'info_droplet.png'
save_figure(fig, str(output))
print(f'Saved {output}')