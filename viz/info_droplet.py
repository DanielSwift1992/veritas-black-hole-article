import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path

fig, ax = plt.subplots(figsize=(6,3))
ax.set_aspect('equal')
ax.axis('off')

# Left: sharded
for x in [-2,-1,0]:
    ax.add_patch(Circle((x,0),0.4,edgecolor='#1f77b4',facecolor='none',linewidth=2))  # blue
ax.text(-1, -1.2, 'Sharded\n(high surface)',ha='center')

# Right: centralized
ax.add_patch(Circle((2,0),1.0,edgecolor='#ff7f0e',facecolor='none',linewidth=2))  # orange
ax.text(2, -1.6, 'Centralized\n(min surface)',ha='center')

plt.xlim(-3.5,4)
plt.ylim(-2,2)
plt.tight_layout()
output = Path(__file__).with_name('info_droplet.png')
plt.savefig(output,dpi=150)
print(f'Saved {output}')