from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt


PALETTE = {
    "blue": "#1f77b4",
    "orange": "#ff7f0e",
    "green": "#2ca02c",
    "red": "#d62728",
    "purple": "#9467bd",
    "grey": "#4d4d4d",
    "light_grid": "#e0e0e0",
}


def init_matplotlib(figure_dpi: int = 160, save_dpi: int = 300) -> None:
    """Initialize consistent, professional matplotlib defaults."""
    plt.style.use("seaborn-v0_8-whitegrid")
    mpl.rcParams.update({
        "figure.dpi": figure_dpi,
        "savefig.dpi": save_dpi,
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 13,
        "axes.edgecolor": PALETTE["grey"],
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": PALETTE["light_grid"],
        "grid.linestyle": "-",
        "grid.alpha": 0.7,
        "legend.frameon": True,
        "legend.fontsize": 11,
        "lines.linewidth": 2.2,
        "lines.markersize": 6,
    })


def apply_axes_style(ax: plt.Axes) -> None:
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linewidth(0.8)


def save_figure(fig: plt.Figure, out_path: str) -> None:
    fig.tight_layout()
    fig.savefig(out_path, transparent=False, bbox_inches="tight")


