from __future__ import annotations

import pathlib
import subprocess
import sys
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult


@plugin("bh_generate_growth_plot")
class GenerateGrowthPlot(BaseCheck):
    """Generate growth curves plot."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        script_path = repo_root / "viz" / "generate_plot.py"
        
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, check=True, 
                                  cwd=repo_root, timeout=30)
            return CheckResult.passed("Growth plot generated successfully")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Growth plot generation failed: {e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"Error generating growth plot: {e}")


@plugin("bh_generate_robust_plot")
class GenerateRobustPlot(BaseCheck):
    """Generate robustness plot."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        script_path = repo_root / "viz" / "robust_plot.py"
        
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, check=True, 
                                  cwd=repo_root, timeout=30)
            return CheckResult.passed("Robust plot generated successfully")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Robust plot generation failed: {e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"Error generating robust plot: {e}")


@plugin("bh_generate_droplet_plot")
class GenerateDropletPlot(BaseCheck):
    """Generate info droplet plot."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        script_path = repo_root / "viz" / "info_droplet.py"
        
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, check=True, 
                                  cwd=repo_root, timeout=30)
            return CheckResult.passed("Droplet plot generated successfully")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Droplet plot generation failed: {e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"Error generating droplet plot: {e}")


@plugin("bh_generate_silence_flow")
class GenerateSilenceFlow(BaseCheck):
    """Generate silence flow diagram."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        script_path = repo_root / "viz" / "silence_flow.py"
        
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, check=True, 
                                  cwd=repo_root, timeout=30)
            return CheckResult.passed("Silence flow diagram generated successfully")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Silence flow generation failed: {e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"Error generating silence flow: {e}")


@plugin("bh_generate_sensitivity_plot")
class GenerateSensitivityPlot(BaseCheck):
    """Generate sensitivity plot t(r) as r → 1⁺."""

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        script_path = repo_root / "viz" / "sensitivity_tr.py"
        if not script_path.exists():
            return CheckResult.failed(f"Script not found: {script_path}")
        try:
            result = subprocess.run([sys.executable, str(script_path)],
                                    capture_output=True, text=True, check=True,
                                    cwd=repo_root, timeout=30)
            return CheckResult.passed("Sensitivity plot generated successfully")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Sensitivity plot generation failed: {e.stderr}")
        except Exception as e:
            return CheckResult.failed(f"Error generating sensitivity plot: {e}")