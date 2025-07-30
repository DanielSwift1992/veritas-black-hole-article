import subprocess, sys, json, pathlib

from bh_core.compiler import compile_program


def test_cli_not(tmp_path):
    # prepare program json
    prog_path = tmp_path/"not.json"
    json.dump([{"op":"NOT","target":1}], prog_path.open("w"))
    # input bits: qubit0 control=0, qubit1 data=1, qubit2 ancilla=0
    result = subprocess.run([sys.executable, "-m", "bh_core.simulate_bh", str(prog_path), "010"], capture_output=True, text=True)
    if result.returncode != 0 and "qutip unavailable" in result.stderr:
        pytest.skip("qutip could not be installed in this environment")
    assert result.returncode == 0
    assert result.stdout.strip() == "001" 