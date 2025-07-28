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
- `get_phi_years.py`: Python script that reproduces **all** timeline tables (quantitative + sensitivity) in the article.
- `LeanBh/`: A Lean 4 library containing the formal proof of the core mathematical claim.
  - `BlackHole.lean`: Proves that for any exponential growth `r > 1`, a finite threshold `N_max` is reached in a finite time `t`.
- `viz/`: Contains scripts for generating visualizations for the article.

## How to Run

### Quick-Start (Reproduce All Tables)

Install dependencies (Lean via `elan`, Python 3.10+, `pip install -e .[dev]`) and run:

```bash
# From project root
lake build                 # formal proofs
python get_phi_years.py    # prints rows for every scenario
python viz/generate_plot.py
```

The first command verifies Lean proofs; the second emits the exact numbers that appear in the article (both quantitative and sensitivity tables). The plot script regenerates `viz/growth_curves.png`.

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

## Assumptions & Limitations

Results depend only on two experimentally verified facts (Landauer’s minimum erase cost, Bekenstein’s density bound) and one weak principle — average information growth r > 1 for any progressing civilisation.  All numeric forecasts additionally assume the illustrative baseline in the article (φ-growth, current N₀, etc.); changing these parameters shifts dates but never removes the finite-time singularity.

## Git hooks / CI discipline

To block commits that break the formal checks, this repository ships with a *pre-commit* hook.

```bash
pip install pre-commit  # one-time
pre-commit install      # installs .git/hooks/pre-commit
```

After that every commit runs `veritas check`; a non-green status aborts the commit. 