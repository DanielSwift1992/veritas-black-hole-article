# ensure path
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from bh_core.compiler import compile_program


def test_compile_not():
    gates = [{"op":"NOT","target":1}]
    prog = compile_program(gates)
    assert prog and prog[0]["op"]=="FLOW" 