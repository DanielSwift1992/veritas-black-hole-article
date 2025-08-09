# Informational Black Holes: The Physical Resolution to the Fermi Paradox

This repository contains the article, code, and formal proof for a model that explains the Fermi Paradox ("The Great Silence") through a physical calculation.

## Core Idea

The repository shows—analytically and formally—that two physical facts (Landauer’s minimum erase cost and the Bekenstein density bound), together with the mild principle “effective information growth r > 1”, force **any** progressing civilisation into a finite-time informational singularity.  Exact timelines depend on parameters; an illustrative baseline (golden-ratio growth) yields ≈192 years.

Civilisations thus converge to compact, silent “computational black holes”: internally active, externally mute.  This provides a physics-based resolution of the Great Silence.

## Contents

- `article_blackhole_inevitable_en.md`: The main article detailing the model, its assumptions, and conclusions.
- `get_phi_years.py`: Python script that reproduces **all** timeline tables (quantitative + sensitivity) in the article.
- `LeanBh/`: A Lean 4 library containing the formal proof of the core mathematical claim.
  - `BlackHole.lean`: Proves that for any exponential growth `r > 1`, a finite threshold `N_max` is reached in a finite time `t`.
- `viz/`: Contains scripts for generating visualizations for the article.
- `probe_cost.py`: script for the Courier-to-Proxima case study.

## How to Run

### Quick-Start (Reproduce All Tables)

Install dependencies (Lean via `elan`, Python 3.10+). Then install system tools and Python libs and run:

```bash
# macOS (Homebrew)
brew install pandoc graphviz

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y pandoc graphviz

# Python deps
pip install -r requirements.txt

# From project root
lake build
veritas check --concurrency=1
```

Scripts rebuild all figures used in the article; `get_phi_years.py` reproduces both main and sensitivity tables.

### Lean Proof Verification

To verify the formal proof, you need Lean 4 and Lake installed.

```bash
# From the project root
lake build
```

### DOCX/PDF export (manual)

```bash
# DOCX with embedded images and size check
pandoc build/artifacts/article_blackhole_inevitable_clean.md \
  -o build/artifacts/article_blackhole_inevitable.docx \
  --standalone --from=markdown+implicit_figures \
  --resource-path build/artifacts:. --dpi=300
stat -f%z build/artifacts/article_blackhole_inevitable.docx
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