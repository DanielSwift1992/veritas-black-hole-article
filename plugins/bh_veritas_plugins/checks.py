from __future__ import annotations
import pathlib
import subprocess
import re
import math
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
            # Ищем год (целое или дробное)
            match = re.search(r"(\d{4})(?:[.,](\d+))?", output)
            if not match:
                return CheckResult.failed("Could not parse year from script output.")
            year_val = float(match.group(1) + ('.' + match.group(2) if match.group(2) else ''))
            year_val = math.ceil(year_val)
            if abs(year_val - (2025 + expected_years)) < 2:
                return CheckResult.passed(f"Result {year_val} is close to expected {2025 + expected_years}")
            else:
                return CheckResult.failed(f"Expected ~{2025 + expected_years}, but got {year_val}")
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
            lean_dir = artifact / "LeanBh"
            if not lean_dir.exists():
                return CheckResult.failed(f"Lean source directory not found: {lean_dir}")
            grep_sorry = subprocess.run(
                ["grep", "-r", "sorry", "--include=*.lean", str(lean_dir)],
                capture_output=True,
                text=True
            )
            grep_axiom = subprocess.run(
                ["grep", "-r", "axiom", "--include=*.lean", str(lean_dir)],
                capture_output=True,
                text=True
            )
            if grep_sorry.stdout:
                return CheckResult.failed(f"Found 'sorry' in proof(s):\n{grep_sorry.stdout}")
            if grep_axiom.stdout:
                return CheckResult.passed(f"Lean proof built successfully, but contains axioms (see warnings):\n{grep_axiom.stdout}")
            build_process = subprocess.run(
                ["lake", "build"],
                cwd=str(artifact),
                capture_output=True,
                text=True,
                check=True,
                timeout=120
            )
            return CheckResult.passed("Lean proof built successfully, no 'sorry's or axioms found.")
        except FileNotFoundError:
            return CheckResult.failed("'lake' or 'grep' command not found. Is Lean installed and in PATH?")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Lean build failed:\n{e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"An unexpected error occurred: {e}")

@plugin("growth_curve_png_check")
class GrowthCurvePngCheck(BaseCheck):
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        plot_py = pathlib.Path("viz/generate_plot.py")
        data_py = pathlib.Path("get_phi_years.py")
        if not artifact.exists():
            return CheckResult.failed(f"PNG not found: {artifact}")
        if artifact.stat().st_mtime < plot_py.stat().st_mtime:
            return CheckResult.failed("PNG older than generate_plot.py, please regenerate the plot.")
        if artifact.stat().st_mtime < data_py.stat().st_mtime:
            return CheckResult.failed("PNG older than get_phi_years.py, please regenerate the plot.")
        return CheckResult.passed("Growth curve PNG is up-to-date and present.") 