"""Generate high-quality flowchart with Graphviz (single External Silence node)."""
import os, subprocess, textwrap, sys

ART_DIR = os.getenv("BH_ARTIFACT_DIR", "build/artifacts")
os.makedirs(ART_DIR, exist_ok=True)

colors = {
    "blue": "#1f77b4",         # edge color (matches Figure 5)
    "blue_fill": "#F9FCFE",     # very light blue
    "orange": "#ff7f0e",       # edge color (matches Figure 5)
    "orange_fill": "#FFFEFB",   # very light orange
    "green": "#4AA564",         # softened green edge
    "green_fill": "#F7FFF7",    # very light green
    "silence_edge": "#d62728",  # subtle red for terminal state
    "silence_fill": "#FFF9F9",  # very light pink
}

dot_template = """
digraph SilenceFlow {
  graph [dpi=180, rankdir=LR, bgcolor="white", size="12,7!", margin="0.2,0.2"];
  node  [shape=box, style="filled", fontname="DejaVu Sans", fontsize=12, color="#4d4d4d", fillcolor="white", fontcolor="black", penwidth=1.2];
  edge  [color="#666666", penwidth=1.4, arrowsize=0.9, arrowhead="vee", splines=true];

  NegNode  [label="Negentropic\nNode", color="BLUE", fillcolor="#F9FCFE", fontcolor="black", style="filled,rounded"];
  Stagnant [label="r ≤ 1\nStagnation", color="ORANGE", fillcolor="#FFFEFB", fontcolor="black", style="filled,rounded"];
  Growth   [label="r > 1\nGrowth", color="ORANGE", fillcolor="#FFFEFB", fontcolor="black", style="filled,rounded"];
  Bound    [label="Bekenstein\nBound", color="GREEN", fillcolor="#F7FFF7", fontcolor="black", style="filled,rounded"];
  Silent   [label="External Silence", shape=box, style="filled,rounded", fillcolor="SILENCE_FILL", fontcolor="black", color="SILENCE_EDGE"];

  NegNode -> Stagnant;
  NegNode -> Growth;
  Growth  -> Bound;
  Stagnant -> Silent;
  Bound    -> Silent;
}
"""
dot = (
    textwrap.dedent(dot_template)
    .replace("BLUE", colors["blue"]) 
    .replace("BLUE_FILL", colors["blue_fill"]) 
    .replace("ORANGE", colors["orange"]) 
    .replace("ORANGE_FILL", colors["orange_fill"]) 
    .replace("GREEN", colors["green"]) 
    .replace("GREEN_FILL", colors["green_fill"]) 
    .replace("SILENCE_EDGE", colors["silence_edge"]) 
    .replace("SILENCE_FILL", colors["silence_fill"]) 
)

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
