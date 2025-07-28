import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path

fig, ax = plt.subplots(figsize=(6,3))
ax.set_aspect('equal')
ax.axis('off')

# Left: sharded
for x in [-2,-1,0]:
    ax.add_patch(Circle((x,0),0.4,edgecolor='steelblue',facecolor='none',linewidth=2))
ax.text(-1, -1, 'Sharded\n(high surface)',ha='center')

# Right: centralized
ax.add_patch(Circle((2,0),1.0,edgecolor='darkgreen',facecolor='none',linewidth=2))
ax.text(2, -1.3, 'Centralized\n(min surface)',ha='center')

plt.xlim(-3.5,4)
plt.ylim(-2,2)
plt.tight_layout()
output = Path(__file__).with_name('info_droplet.png')
plt.savefig(output,dpi=150)
print(f'Saved {output}')