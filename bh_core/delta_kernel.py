import numpy as np
import qutip as qt
from typing import List, Dict

__all__ = ["DeltaComputer"]


def _build_flow_unitary(n: int, ctrl: int, t1: int, t2: int) -> qt.Qobj:
    """(Anti)-controlled SWAP: swap t1,t2 iff ctrl qubit is |0>.
    Works for any n≥3 with ctrl<t1<t2.
    """
    dim = 2 ** n
    U = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        bits = [(col >> (n - 1 - k)) & 1 for k in range(n)]
        if bits[ctrl] == 0:
            bits[t1], bits[t2] = bits[t2], bits[t1]
        row = 0
        for b in bits:
            row = (row << 1) | b
        U[row, col] = 1.0
    return qt.Qobj(U, dims=[[2] * n, [2] * n])


class DeltaComputer:
    """Minimal reversible Δ-Kernel simulator on arbitrary number of qubits."""

    def __init__(self, num_qubits: int = 0):
        self.num_qubits = num_qubits
        self.rho: qt.Qobj
        if num_qubits == 0:
            self.rho = None  # will set on first accrete
        else:
            plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit().proj()
            self.rho = qt.tensor([plus for _ in range(num_qubits)])

    # ───────────────────────────────────────────── Accretion
    def accrete(self, state: qt.Qobj):
        """Append single-qubit *density matrix* to horizon."""
        if state.dims != [[2], [2]]:
            if state.isket:
                state = state.proj()
            else:
                raise ValueError("State must be single-qubit ket or density matrix")
        if self.rho is None:
            self.rho = state
        else:
            self.rho = qt.tensor(self.rho, state)
        self.num_qubits += 1

    # ───────────────────────────────────────────── Primitive
    def flow(self, ctrl: int, t1: int, t2: int):
        if not (0 <= ctrl < t1 < t2 < self.num_qubits):
            raise ValueError("Require ctrl < t1 < t2 within current qubits")
        U = _build_flow_unitary(self.num_qubits, ctrl, t1, t2)
        self.rho = U * self.rho * U.dag()

    # ───────────────────────────────────────────── Program execution
    def execute(self, program: List[Dict]):
        """Execute compiled list of {'op':'FLOW','ctrl':..,'t1':..,'t2':..}."""
        for inst in program:
            if inst["op"] != "FLOW":
                raise ValueError("Program must be pre-compiled to FLOW ops")
            self.flow(inst["ctrl"], inst["t1"], inst["t2"])

    # ───────────────────────────────────────────── Observables
    def measure_z(self, qubit: int = 0) -> float:
        if self.rho is None:
            raise RuntimeError("No state loaded")
        Z = qt.sigmaz()
        return qt.expect(Z, self.rho.ptrace(qubit))

    def ent_matrix(self) -> np.ndarray:
        m = np.zeros((self.num_qubits, self.num_qubits))
        for i in range(self.num_qubits):
            for j in range(i + 1, self.num_qubits):
                ent = qt.entropy_vn(self.rho.ptrace([i, j]))
                m[i, j] = m[j, i] = ent
        return m

    def trace_norm(self) -> float:
        return abs(self.rho.tr()) if self.rho is not None else 0.0 