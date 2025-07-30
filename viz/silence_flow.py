"""Generate high-quality flowchart with Graphviz (single External Silence node)."""
import os, subprocess, textwrap, sys

ART_DIR = os.getenv("BH_ARTIFACT_DIR", "build/artifacts")
os.makedirs(ART_DIR, exist_ok=True)

colors = {
    "blue": "#1f77b4",
    "orange": "#ff7f0e",
    "green": "#2ca02c",
    "yellow": "#fff5cc",
}

dot = textwrap.dedent(f"""
digraph SilenceFlow {{
  graph [dpi=120, rankdir=LR, bgcolor="white", size="12,7!", margin="0.0,0.0"];
  node  [shape=box, style="rounded", fontname="Helvetica", fontsize=12, color="#4d4d4d", fillcolor="white", fontcolor="black"];

  NegNode  [label="Negentropic\nNode", color="{colors['blue']}", fontcolor="black"];
  Stagnant [label="r ≤ 1\nStagnation", color="{colors['orange']}", fontcolor="black"];
  Growth   [label="r > 1\nGrowth", color="{colors['orange']}", fontcolor="black"];
  Bound    [label="Bekenstein\nBound", color="{colors['green']}", fontcolor="black"];
  Silent   [label="External Silence", shape=box, style="rounded,filled", fillcolor="{colors['yellow']}", fontcolor="black", color="#4d4d4d"];

  NegNode -> Stagnant;
  NegNode -> Growth;
  Growth  -> Bound;
  Stagnant -> Silent;
  Bound    -> Silent;

  {{ rank=same; Stagnant; Growth }}\n  {{ rank=sink; Silent }}
}}
""")

try:
    dot_bin = "dot"
    # ensure graphviz installed
    subprocess.run([dot_bin, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
except Exception:
    sys.exit("Graphviz 'dot' not found. Please install Graphviz.")

DOT_PATH = os.path.join(ART_DIR, "silence_flow.dot")
with open(DOT_PATH, "w", encoding="utf-8") as f:
    f.write(dot)

PNG_PATH = os.path.join(ART_DIR, "silence_flow.png")
subprocess.run(["dot", "-Tpng", DOT_PATH, "-o", PNG_PATH], check=True)
print("Saved", PNG_PATH)
