# add repo root to path and ensure qutip present
import sys, pathlib, subprocess, importlib.util

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import pytest

spec = importlib.util.find_spec("qutip")
if spec is None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qutip==5.2.0", "--quiet"])
    except Exception:
        pytest.skip("qutip unavailable and installation failed", allow_module_level=True)

import qutip as qt  # noqa: E402

from bh_core.delta_kernel import DeltaComputer


def test_flow_not():
    comp = DeltaComputer()
    comp.accrete(qt.basis(2,0))   # qubit0 control |0>
    comp.accrete(qt.basis(2,1))   # qubit1 data |1>
    comp.accrete(qt.basis(2,0))   # qubit2 ancilla
    # need ctrl<t1<t2, so reorder: ctrl=0, t1=1, t2=2  (we'll swap 1<->2)
    comp.flow(0,1,2)
    z = comp.measure_z(0)
    # after swap data becomes |0>
    assert z > 0.9
    assert abs(comp.trace_norm()-1)<1e-6 