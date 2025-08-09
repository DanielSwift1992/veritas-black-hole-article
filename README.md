# Informational Black Holes: The Physical Resolution to the Fermi Paradox

This repository contains the article, code, and formal proof for a model that explains the Fermi Paradox ("The Great Silence") through a physical calculation.

## Core Idea

The repository shows—analytically and formally—that two physical facts (Landauer’s minimum erase cost and the Bekenstein density bound), together with the mild principle “effective information growth r > 1”, force any progressing civilization into a finite‑time informational singularity. Exact timelines depend on parameters; an illustrative, conservative baseline (φ‑growth) yields ≈192 years.

Externally, systems become silent, information‑saturated states (an “informational black hole” in the article’s terminology). Gravitational collapse is an extreme case; the key conclusion is external silence.

## Contents

- `article_blackhole_inevitable_en.md`: the main article.
- `scripts/get_phi_years.py`: reproduces timeline tables (main + sensitivity).
- `scripts/probe_cost.py`: Courier‑to‑Proxima case study numbers.
- `LeanBh/`: Lean 4 proofs.
  - `BlackHole.lean`: finite‑time threshold for any `r > 1`.
  - `PhiMinimal.lean`: φ as minimal loss‑free baseline in a monotone model.
- `viz/`: scripts for all figures (growth curves, robustness, sensitivity, droplet, flow).
- `logic-graph.yml` + `plugins/`: Veritas graph and custom checks.

## How to Run

### One‑command reproduction (recommended)

Install dependencies (Lean via `elan`, Python 3.10+, `pip install -e .[dev]`) and run:

```bash
# From project root
veritas check --concurrency=1   # full pipeline: proofs, data, figures, PDF/DOCX
```

This regenerates all data, checks Lean proofs, refreshes figures, and compiles the PDF. For journals that require Word, you can export DOCX with embedded images manually:

```bash
pandoc build/artifacts/article_blackhole_inevitable_clean.md \
  -o build/artifacts/article_blackhole_inevitable.docx \
  --standalone --from=markdown+implicit_figures \
  --resource-path build/artifacts:. --dpi=300
```

### Manual steps (if needed)

```bash
# Proofs
lake build

# Tables
python scripts/get_phi_years.py --csv

# Figures
python viz/generate_plot.py
python viz/robust_plot.py
python viz/sensitivity_tr.py
python viz/silence_flow.py
python viz/info_droplet.py
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
python viz/generate_plot.py
```

## Assumptions & Limitations

Results depend on two experimentally verified facts (Landauer’s minimum erase cost, Bekenstein’s density bound) and one weak principle — average information growth r > 1 for any progressing civilization. Numeric forecasts additionally assume the article’s conservative baseline (φ‑growth, current N₀, etc.); changing these parameters shifts dates but does not remove the finite‑time singularity.

## Git hooks / CI discipline

To block commits that break the formal checks, this repository ships with a *pre-commit* hook.

```bash
pip install pre-commit  # one-time
pre-commit install      # installs .git/hooks/pre-commit
```

After that every commit runs `veritas check`; a non‑green status aborts the commit.