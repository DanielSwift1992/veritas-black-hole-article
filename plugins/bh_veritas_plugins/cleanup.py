from __future__ import annotations

import pathlib
import shutil
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult


@plugin("bh_cleanup_artifacts")
class CleanupArtifacts(BaseCheck):
    """Clean artifacts directory before regeneration."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        artifacts_dir = repo_root / "build" / "artifacts"
        
        if not artifacts_dir.exists():
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            return CheckResult.passed("Created clean artifacts directory")
        
        try:
            # Remove and recreate directory for clean slate
            shutil.rmtree(artifacts_dir)
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            return CheckResult.passed("Cleaned artifacts directory")
            
        except Exception as e:
            return CheckResult.failed(f"Cleanup failed: {e}")