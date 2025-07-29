from __future__ import annotations
import pathlib
import subprocess
import re
import math
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult
import sys
import csv
from typing import Dict, Tuple

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
            # Parse first 4-digit year from script output
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
            grep_admit = subprocess.run(
                ["grep", "-r", "admit", "--include=*.lean", str(lean_dir)],
                capture_output=True,
                text=True,
            )
            # Detect actual axiom declarations (line starting with optional spaces then 'axiom')
            grep_axiom = subprocess.run(
                [
                    "grep",
                    "-rE",
                    "^\\s*axiom\\b",
                    "--include=*.lean",
                    str(lean_dir),
                ],
                capture_output=True,
                text=True,
            )
            # Detect "too-trivial" proofs that may hide axioms behind `exact`.
            grep_exact = subprocess.run(
                [
                    "grep",
                    "-r",
                    "exact ",
                    "--include=*.lean",
                    str(lean_dir),
                ],
                capture_output=True,
                text=True,
            )
            suspicious_lines = [
                ln for ln in grep_exact.stdout.strip().split("\n") if "exact ⟨phi" in ln
            ]
            # Detect trivial 'by rfl' proofs that ignore premises.
            grep_rfl = subprocess.run(
                [
                    "grep",
                    "-r",
                    "by rfl",
                    "--include=*.lean",
                    str(lean_dir),
                ],
                capture_output=True,
                text=True,
            )
            if grep_rfl.stdout:
                suspicious_lines.extend(grep_rfl.stdout.strip().split("\n"))

            if suspicious_lines:
                return CheckResult.failed(
                    "Suspicious trivial proofs detected that may mask axioms:\n" + "\n".join(suspicious_lines)
                )
            if grep_sorry.stdout:
                return CheckResult.failed(f"Found 'sorry' in proof(s):\n{grep_sorry.stdout}")
            if grep_admit.stdout:
                return CheckResult.failed(f"Found 'admit' in proof(s):\n{grep_admit.stdout}")
            if grep_axiom.stdout:
                return CheckResult.failed(
                    "Axiom declaration(s) found (proof must be axioms-free):\n" + grep_axiom.stdout
                )
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

# Remove bespoke implementation; reuse generic factory below.


# Generic PNG freshness checker factory
def _png_check(name: str, png_path: str, script_path: str):
    @plugin(name)
    class _Check(BaseCheck):
        def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
            repo_root = pathlib.Path(__file__).resolve().parents[2]
            png = repo_root / png_path
            script = repo_root / script_path
            if not png.exists():
                return CheckResult.failed(f"PNG not found: {png}")
            if png.stat().st_mtime < script.stat().st_mtime:
                return CheckResult.failed(f"PNG older than {script_path}, regenerate.")
            return CheckResult.passed(f"{png_path} is up-to-date")

    return _Check

# Register two more PNG checks
robust_png_check = _png_check("robust_png_check", "viz/robust_recal.png", "viz/robust_plot.py")
droplet_png_check = _png_check("droplet_png_check", "viz/info_droplet.png", "viz/info_droplet.py")
growth_curve_png_check = _png_check("growth_curve_png_check", "viz/growth_curves.png", "viz/generate_plot.py")

@plugin("article_table_check")
class ArticleTableCheck(BaseCheck):
    """Verify that the numeric values in the Markdown table match model calculations."""

    N0 = 1.448e24
    N_MAX = 1.74e64
    START_YEAR = 2025

    # Mapping: label -> (growth_rate r, N_max multiplicative factor)
    SCENARIOS = {
        "Conservative": (1.23, 1),
        "Big-Data": (1.40, 1),
        "φ Baseline": ((1 + 5 ** 0.5) / 2, 1),
        "Larger BH": ((1 + 5 ** 0.5) / 2, 100),  # 1 cm → N_max ×100
        "Partial deletion allowed": (1.50, 1),
        "Massive expansion": ((1 + 5 ** 0.5) / 2, 1e10),
        "Doppler recalibration": ((1 + 5 ** 0.5) / 2, 2),
    }

    def _calc_years(self, r: float, n_factor: float = 1) -> tuple[int, int]:
        import math
        t = math.log((self.N_MAX * n_factor) / self.N0) / math.log(r)
        years = math.ceil(t)
        return years, self.START_YEAR + years

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        """Compare CSV produced by get_phi_years.py with tables inside the article."""
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        script_path = repo_root / "get_phi_years.py"
        if not script_path.exists():
            return CheckResult.failed("get_phi_years.py not found in repository root.")

        try:
            proc = subprocess.run([
                sys.executable,
                str(script_path),
                "--csv",
            ], capture_output=True, text=True, check=True, timeout=15)
        except Exception as e:
            return CheckResult.failed(f"Failed to run get_phi_years.py: {e}")

        csv_lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        reader = csv.DictReader(csv_lines)
        expected: Dict[str, Tuple[int, int]] = {}
        for row in reader:
            label = row["Scenario"].strip()
            expected[label] = (int(row["Years"]), int(row["Year"]))

        article_path = repo_root / "article_blackhole_inevitable_en.md"
        if not article_path.exists():
            return CheckResult.failed(f"Article not found: {article_path}")
        text = article_path.read_text(encoding="utf-8")

        failures = []
        seen_labels = set()
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) != 4:
                continue
            label, _r_str, years_str, year_str = parts
            label_clean = label.split("(")[0].strip()
            if label_clean not in expected:
                continue
            seen_labels.add(label_clean)
            try:
                years = int(years_str)
                year = int(year_str)
            except ValueError:
                failures.append(f"Non-integer values for {label_clean} row in article.")
                continue

            exp_years, exp_year = expected[label_clean]
            if abs(years - exp_years) > 1 or abs(year - exp_year) > 1:
                failures.append(f"Mismatch for {label_clean}: article has {years}/{year}, expected {exp_years}/{exp_year}.")

        missing = set(expected.keys()) - seen_labels
        if missing:
            failures.append("Rows missing in article: " + ", ".join(sorted(missing)))

        if failures:
            return CheckResult.failed("Table mismatch:\n" + "\n".join(failures))

        return CheckResult.passed("Article tables are in sync with get_phi_years.py output.")

# ---------------------------------------------------------------------------
# Centralization energy check
# ---------------------------------------------------------------------------


@plugin("centralization_energy_check")
class CentralizationEnergyCheck(BaseCheck):
    """Verify that sharded design is always more expensive than centralized for default params."""

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        script = repo_root / "get_phi_years.py"
        if not script.exists():
            return CheckResult.failed("get_phi_years.py not found")

        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--compare-sharded", "4", "1000"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
        except Exception as e:
            return CheckResult.failed(f"Failed to run comparison: {e}")

        out = proc.stdout.strip()
        if out == "PASS":
            return CheckResult.passed("Sharded energy ≥ centralized energy as expected.")
        return CheckResult.failed("Energy inequality not satisfied (output: " + out + ")") 

# ---------------------------------------------------------------------------
# Storage economy table check
# ---------------------------------------------------------------------------

@plugin("storage_table_check")
class StorageTableCheck(BaseCheck):
    """Verify that the Information Economics table in the article matches storage_crossover.py output."""

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        script = repo_root / "storage_crossover.py"
        article = repo_root / "article_blackhole_inevitable_en.md"
        if not script.exists():
            return CheckResult.failed("storage_crossover.py not found")
        if not article.exists():
            return CheckResult.failed("Article file not found")

        try:
            proc = subprocess.run([
                sys.executable,
                str(script),
                "--csv",
            ], capture_output=True, text=True, check=True, timeout=10)
        except Exception as e:
            return CheckResult.failed(f"Failed to run storage_crossover.py: {e}")

        csv_lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        reader = csv.DictReader(csv_lines)
        expected: Dict[int, Tuple[float, float]] = {}
        for row in reader:
            yr = int(row["Year"])
            ratio = float(row["RatioStoreToDelete"])
            transmit_ratio = float(row["RatioStoreToTransmit"])
            expected[yr] = (ratio, transmit_ratio)

        # Locate table lines in article (look for '| 2106 |' etc.)
        failures = []
        for line in article.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("|"):
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if len(parts) < 4:
                    continue
                try:
                    yr = int(parts[0])
                    ratio_text = parts[4]
                    log_text = parts[5]
                    transmit_text = parts[6]
                    ratio = float(ratio_text)
                    transmit_ratio = float(transmit_text)
                except ValueError:
                    continue
                if yr in expected:
                    exp_ratio, exp_transmit = expected[yr]
                    if abs(math.log10(ratio) - math.log10(exp_ratio)) > 0.5 or abs(math.log10(transmit_ratio) - math.log10(exp_transmit)) > 0.5:
                        failures.append(f"Mismatch for year {yr}: ratios article {ratio:.1e}/{transmit_ratio:.1e} vs script {exp_ratio:.1e}/{exp_transmit:.1e}")
                    expected.pop(yr)
        if expected:
            failures.append("Article missing rows for years: " + ", ".join(map(str, expected.keys())))
        if failures:
            return CheckResult.failed("Storage table mismatch:\n" + "\n".join(failures))
        return CheckResult.passed("Storage economics table matches script output.") 