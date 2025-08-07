#!/usr/bin/env python3
"""
Plot sensitivity of time-to-bound t(r) = ln(N_max/N0)/ln(r) for r in [1.0001, 1.8].
This illustrates logarithmic stretching as r → 1⁺ without changing finiteness.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import math
import os

N0 = 1.448e24
N_MAX = 1.74e64

def main() -> None:
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

    r_vals = np.concatenate([
        np.linspace(1.0001, 1.01, 200),
        np.linspace(1.01, 1.2, 200),
        np.linspace(1.2, 1.8, 200),
    ])
    t_vals = np.log(N_MAX / N0) / np.log(r_vals)

    ax.plot(r_vals, t_vals, color="#1f77b4", linewidth=2.2)
    ax.set_xlabel("Growth factor r", fontsize=13)
    ax.set_ylabel("Years to threshold t(r)", fontsize=13)
    ax.set_title("Sensitivity of time-to-bound t(r) as r → 1⁺", fontsize=16, pad=12)
    ax.set_xlim(1.0001, 1.8)
    ax.set_ylim(0, min(1.1*max(t_vals), 1.1*t_vals[-1]))
    ax.grid(True, which="both", ls="-", color="#e0e0e0", alpha=0.7)
    fig.tight_layout()

    out_dir = os.getenv("BH_ARTIFACT_DIR", "build/artifacts")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "sensitivity_tr.png")
    plt.savefig(out_path, transparent=False, bbox_inches='tight')
    print(f"Plot saved to {out_path}")

if __name__ == "__main__":
    main()


