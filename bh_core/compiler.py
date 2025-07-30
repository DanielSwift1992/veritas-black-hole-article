import json
from typing import List, Dict

__all__ = ["compile_program"]


def compile_program(gate_list: List[Dict]) -> List[Dict]:
    """Turn high-level reversible gates into primitive FLOW instructions.

    Supported gates:
    ● NOT   {"op":"NOT",  "target":i}
    ● CNOT  {"op":"CNOT", "control":c, "target":t}
    ● TOFF  {"op":"TOFF","c1":c1,"c2":c2,"target":t}
    Output list items: {op:"FLOW", ctrl:int, t1:int, t2:int}
    """
    flows = []
    for g in gate_list:
        op = g["op"].upper()
        if op == "NOT":
            t = g["target"]
            if t == 0:
                raise ValueError("NOT target cannot be 0 – reserve qubit0 as control |0>")
            flows.append({"op": "FLOW", "ctrl": 0, "t1": t, "t2": t + 1})
        elif op == "CNOT":
            c, t = g["control"], g["target"]
            flows.append({"op": "FLOW", "ctrl": c, "t1": c, "t2": t})
        elif op == "TOFF":
            c1, c2, t = g["c1"], g["c2"], g["target"]
            # Decompose Toffoli into 2 controlled swaps using c1 as control on (c2,t)
            flows.append({"op": "FLOW", "ctrl": c1, "t1": c2, "t2": t})
            flows.append({"op": "FLOW", "ctrl": c2, "t1": c1, "t2": t})
            flows.append({"op": "FLOW", "ctrl": c1, "t1": c2, "t2": t})
        else:
            raise ValueError(f"Unsupported gate {op}")
    return flows


def load_json(path: str) -> List[Dict]:
    with open(path, "r") as f:
        return json.load(f) 