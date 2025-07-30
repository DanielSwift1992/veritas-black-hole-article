import argparse, json, sys, subprocess, importlib.util

# ensure qutip present even in CI where wheel absent
if importlib.util.find_spec("qutip") is None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qutip==5.2.0", "--quiet", "--break-system-packages"])
    except Exception:
        print("qutip unavailable and installation failed", file=sys.stderr)
        sys.exit(1)

import qutip as qt
from bh_core.delta_kernel import DeltaComputer
from bh_core.compiler import compile_program, load_json


def parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Black-Hole Δ-Kernel simulator")
    p.add_argument("program", help="Path to JSON gate list")
    p.add_argument("input", help="bitstring input, e.g. 1010")
    p.add_argument("--steps", type=int, default=1, help="Execute program N times (for benchmark)")
    return p.parse_args()


def bit_to_state(b: str) -> qt.Qobj:
    return qt.basis(2, int(b))


def main():
    args = parse()
    gate_list = load_json(args.program)
    prog = compile_program(gate_list)

    comp = DeltaComputer()
    # accrete input bits
    for bit in args.input.strip():
        if bit not in "01":
            print("Input must be bitstring", file=sys.stderr)
            sys.exit(1)
        comp.accrete(bit_to_state(bit))

    comp.execute(prog)
    out_bits = "".join("0" if comp.measure_z(i) > 0 else "1" for i in range(comp.num_qubits))
    print(out_bits)


if __name__ == "__main__":
    main() 