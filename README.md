# A Physical Calculation for the Great Silence

This repository contains the article, code, and formal proof for a model that explains the Fermi Paradox ("The Great Silence") through a physical calculation.

## Core Idea

The model demonstrates that any civilization driven by efficiency will, by calculation, inevitably vanish behind a physical singularity. The logic is straightforward:

1.  **Fact:** Erasing data has a real, minimum energy cost (Landauer's principle). Storing it has a physical density limit (the Bekenstein bound). Both are experimentally verified.
2.  **Rationality:** An advanced AI or economy will always minimize energy expenditure. Thus, it will avoid the perpetual "tax" of deleting data, opting instead for lossless, exponential growth.
3.  **Calculation:** An exponential function with a growth rate `r > 1` *will* cross a finite limit. Given today's data volume and an optimal growth model, this physical singularity is reached in ≈191 years.

Civilizations don't die out; they optimize themselves into computational black holes—infinitely dense, internally active, but externally silent. This is why the sky is quiet.

## Contents

- `article_blackhole_inevitable_en.md`: The main article detailing the model, its assumptions, and conclusions.
- `ai_black_hole_time_to_threshold.py`: A Python script to calculate the time to the singularity based on various growth rates.
- `LeanBh/`: A Lean 4 library containing the formal proof of the core mathematical claim.
  - `BlackHole.lean`: Proves that for any exponential growth `r > 1`, a finite threshold `N_max` is reached in a finite time `t`.
- `viz/`: Contains scripts for generating visualizations for the article.

## How to Run

### Python Calculation

To see the time-to-singularity calculations:

```bash
python ai_black_hole_time_to_threshold.py
```

### Lean Proof Verification

To verify the formal proof, you need Lean 4 and Lake installed.

```bash
# From the project root
lake build
```

### Visualization

To generate the growth curve plot:

```bash
cd viz
python generate_plot.py
``` 