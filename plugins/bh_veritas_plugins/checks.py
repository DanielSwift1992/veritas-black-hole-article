from __future__ import annotations
import pathlib
import subprocess
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult

@plugin("bh_python_timeline_check")
class PythonTimelineCheck(BaseCheck):
    """
    Checks that a Python script runs and outputs an expected numeric value.
    """
    def run(self, artifact: pathlib.Path, *, expected_years: int, **kw) -> CheckResult:
        script_name = "get_phi_years.py"
        script_path = artifact / script_name
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        print(f"[DEBUG] Will run script: {script_path}")
        try:
            process = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            output = process.stdout
            for line in output.splitlines():
                if line.strip().isdigit():
                    try:
                        output_years = int(float(line.strip().split()[-1]))
                        break
                    except Exception:
                        continue
            else:
                return CheckResult.failed("Could not parse script output as a year.")
            if abs(output_years - (2025 + expected_years)) < 2:
                return CheckResult.passed(f"Result {output_years} is close to expected {2025 + expected_years}")
            else:
                return CheckResult.failed(f"Expected ~{2025 + expected_years}, but got {output_years}")
        except FileNotFoundError:
            return CheckResult.failed("Python interpreter not found.")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Script failed with error:\n{e.stderr}")
        except (ValueError, TypeError) as e:
            return CheckResult.failed(f"Could not parse script output as a number: {e}")
        except Exception as e:
            return CheckResult.failed(f"An unexpected error occurred: {e}")

@plugin("bh_lean_proof_check")
class LeanProofCheck(BaseCheck):
    """
    Checks that a Lean project builds successfully and contains no 'sorry's.
    """
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        if not artifact.is_dir():
            return CheckResult.failed(f"Artifact {artifact} is not a Lean project directory.")

        try:
            # 1. Check for 'sorry' only in LeanBh/*.lean
            lean_dir = artifact / "LeanBh"
            if not lean_dir.exists():
                return CheckResult.failed(f"Lean source directory not found: {lean_dir}")
            grep_process = subprocess.run(
                ["grep", "-r", "sorry", "--include=*.lean", str(lean_dir)],
                capture_output=True,
                text=True
            )
            if grep_process.stdout:
                return CheckResult.failed(f"Found 'sorry' in proof(s):\n{grep_process.stdout}")

            # 2. Build the project
            build_process = subprocess.run(
                ["lake", "build"],
                cwd=str(artifact),
                capture_output=True,
                text=True,
                check=True,
                timeout=120
            )
            return CheckResult.passed("Lean proof built successfully, no 'sorry's found.")

        except FileNotFoundError:
            return CheckResult.failed("'lake' or 'grep' command not found. Is Lean installed and in PATH?")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Lean build failed:\n{e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"An unexpected error occurred: {e}") 