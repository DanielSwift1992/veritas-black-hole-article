from __future__ import annotations

import pathlib
import subprocess
import tempfile
import re
import zipfile
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult

@plugin("bh_pandoc_check")
class PandocCheck(BaseCheck):
    """Check that pandoc is installed for LaTeX compilation."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        try:
            subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
            return CheckResult.passed("Pandoc is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            return CheckResult.failed("Pandoc not found. Install with: brew install pandoc (macOS) or apt-get install pandoc (Ubuntu)")


@plugin("bh_latex_pdf_compile")
class LaTeXPDFCompiler(BaseCheck):
    """Compile Markdown article to PDF using pandoc and pdflatex."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        # Derive repository root from the provided artifact path (which points to the PDF)
        def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
            current = start.resolve()
            for _ in range(8):
                if (current / "logic-graph.yml").exists() or (current / ".git").exists() or (current / "lake-manifest.json").exists():
                    return current
                if current.parent == current:
                    break
                current = current.parent
            return start.resolve()

        repo_root = _find_repo_root(pathlib.Path(artifact))
        article_path = repo_root / "build" / "artifacts" / "article_blackhole_inevitable_clean.md"
        
        if not article_path.exists():
            return CheckResult.failed(f"Article not found: {article_path}")
        
        try:
            # Ensure all expected images exist before compilation
            images_and_scripts = [
                (repo_root / "build" / "artifacts" / "growth_curves.png", repo_root / "viz" / "generate_plot.py"),
                (repo_root / "build" / "artifacts" / "robust_recal.png", repo_root / "viz" / "robust_plot.py"),
                (repo_root / "build" / "artifacts" / "sensitivity_tr.png", repo_root / "viz" / "sensitivity_tr.py"),
                (repo_root / "build" / "artifacts" / "silence_flow.png", repo_root / "viz" / "silence_flow.py"),
                (repo_root / "build" / "artifacts" / "info_droplet.png", repo_root / "viz" / "info_droplet.py"),
            ]
            import sys
            for img, script in images_and_scripts:
                try:
                    if (not img.exists()) or (img.stat().st_mtime < script.stat().st_mtime):
                        subprocess.run([sys.executable, str(script)], cwd=str(repo_root), check=True)
                except Exception:
                    # Continue; pandoc will fail later with a clear message if missing
                    pass

            # Convert to PDF directly with pandoc using the clean markdown path
            output_dir = repo_root / "build" / "artifacts"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_pdf = output_dir / "article_blackhole_inevitable.pdf"

            # Ensure images referenced by relative paths are found via resource-path (search in artifacts dir first)
            resource_path = f"{repo_root / 'build' / 'artifacts'}:{repo_root}"

            try:
                result = subprocess.run([
                    "pandoc",
                    str(article_path),
                    "-o", str(output_pdf),
                    "--standalone",
                    "--from=markdown+implicit_figures",
                    "--resource-path", resource_path,
                    "--pdf-engine=xelatex",
                    "--table-of-contents",
                    "--number-sections",
                    "-V", "geometry:margin=2cm",
                    "-V", "fontsize=12pt",
                    "-V", "linestretch=1.2",
                    "-V", "title=Informational Black Holes: The Physical Resolution to the Fermi Paradox",
                    "-V", "author=Daniil Strizhov",
                    "-V", "toc-title=Contents",
                    "-V", "tables=true",
                    "-V", "longtable=true",
                    "--metadata", "title=Informational Black Holes: The Physical Resolution to the Fermi Paradox",
                    "--shift-heading-level-by=-1",
                    "--dpi=300",
                ], capture_output=True, text=True, check=True)

                if not output_pdf.exists():
                    return CheckResult.failed(f"Pandoc reported success, but PDF not found at {output_pdf}")
                return CheckResult.passed(f"PDF compiled: {output_pdf}")

            except subprocess.CalledProcessError as e:
                return CheckResult.failed(f"Pandoc failed: {e.stderr}")
            except FileNotFoundError:
                return CheckResult.failed("Pandoc not found. Please install pandoc and pdflatex.")
                
        except Exception as e:
            return CheckResult.failed(f"PDF compilation failed: {e}")


@plugin("bh_clean_markdown_compile")
class CleanMarkdownCompiler(BaseCheck):
    """Generate a clean markdown version without Veritas tags."""
    
    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo_root = artifact
        article_path = repo_root / "article_blackhole_inevitable_en.md"
        
        if not article_path.exists():
            return CheckResult.failed(f"Article not found: {article_path}")
        
        try:
            # Read the markdown content with error handling
            try:
                content = article_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Try with different encoding if UTF-8 fails
                content = article_path.read_text(encoding="utf-8", errors="ignore")
            
            # Remove Veritas VALUE tags but keep the values
            import re
            
            # Replace <!--VALUE:name-->value<!--END:name--> with just value
            def replace_value_tag(match):
                return match.group(1)  # Return just the value part
            
            pattern = r'<!--VALUE:[^>]+-->([^<]*)<!--END:[^>]+-->'
            clean_content = re.sub(pattern, replace_value_tag, content)
            
            # Remove any remaining HTML comments
            clean_content = re.sub(r'<!--[^>]*-->', '', clean_content)
            
            # Clean up multiple newlines
            clean_content = re.sub(r'\n\n\n+', '\n\n', clean_content)

            # Rewrite image paths that point to build/artifacts/ to be relative (filenames only)
            # More robust patterns to catch edge-cases
            # 1) Standard image link
            clean_content = re.sub(r'(!\[[^\]]*\]\()\.?/?build/artifacts/([^\)]+)\)', r'\1\2)', clean_content)
            # 2) Fallback raw replacement if any residual
            clean_content = clean_content.replace('](build/artifacts/', '](')
            
            # Save clean markdown
            output_dir = repo_root / "build" / "artifacts"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            clean_md_path = output_dir / "article_blackhole_inevitable_clean.md"
            clean_md_path.write_text(clean_content, encoding="utf-8")
            
            return CheckResult.passed(f"Clean markdown generated: {clean_md_path}")
            
        except Exception as e:
            return CheckResult.failed(f"Clean markdown generation failed: {e}")


@plugin("bh_docx_compile")
class MDPIWordExporter(BaseCheck):
    """Export the clean markdown to a Word .docx suitable for MDPI submission."""

    def _find_repo_root(self, start: pathlib.Path) -> pathlib.Path:
        current = start.resolve()
        for _ in range(8):  # avoid infinite climbs
            if (current / "logic-graph.yml").exists() or (current / ".git").exists() or (current / "lake-manifest.json").exists():
                return current
            if current.parent == current:
                break
            current = current.parent
        return start.resolve()

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        # Support being called with either repo root or a target file under build/artifacts
        art_path = pathlib.Path(artifact)
        repo_root = self._find_repo_root(art_path if art_path.exists() else pathlib.Path.cwd())

        # Ensure all expected images exist before DOCX compilation
        try:
            images_and_scripts = [
                (repo_root / "build" / "artifacts" / "growth_curves.png", repo_root / "viz" / "generate_plot.py"),
                (repo_root / "build" / "artifacts" / "robust_recal.png", repo_root / "viz" / "robust_plot.py"),
                (repo_root / "build" / "artifacts" / "sensitivity_tr.png", repo_root / "viz" / "sensitivity_tr.py"),
                (repo_root / "build" / "artifacts" / "silence_flow.png", repo_root / "viz" / "silence_flow.py"),
                (repo_root / "build" / "artifacts" / "info_droplet.png", repo_root / "viz" / "info_droplet.py"),
            ]
            for img, script in images_and_scripts:
                try:
                    if (not img.exists()) or (img.stat().st_mtime < script.stat().st_mtime):
                        subprocess.run([sys.executable, str(script)], cwd=str(repo_root), check=True)
                except Exception:
                    pass
        except Exception:
            pass

        artifacts_dir = repo_root / "build" / "artifacts"
        clean_md = artifacts_dir / "article_blackhole_inevitable_clean.md"
        if not clean_md.exists():
            return CheckResult.failed(f"Clean markdown not found: {clean_md}")

        artifacts_dir.mkdir(parents=True, exist_ok=True)
        output_docx = artifacts_dir / "article_blackhole_inevitable.docx"

        try:
            # Use the exact command that is known to embed images correctly
            result = subprocess.run([
                "pandoc",
                "build/artifacts/article_blackhole_inevitable_clean.md",
                "-o", "build/artifacts/article_blackhole_inevitable.docx",
                "--standalone",
                "--from=markdown+implicit_figures",
                "--resource-path", "build/artifacts:.",
                "--dpi=300",
            ], check=True, capture_output=True, text=True, cwd=str(repo_root))
            # If DOCX is suspiciously small, retry from artifacts dir with local resource-path and embed
            try:
                if output_docx.stat().st_size < 200000:
                    subprocess.run([
                        "pandoc",
                        "article_blackhole_inevitable_clean.md",
                        "-o", "article_blackhole_inevitable.docx",
                        "--standalone",
                        "--from=markdown+implicit_figures",
                        "--resource-path", ".",
                        "--dpi=300",
                    ], check=True, capture_output=True, text=True, cwd=str(artifacts_dir))
            except Exception:
                pass
            return CheckResult.passed(f"DOCX compiled: {output_docx}")
        except subprocess.CalledProcessError as e:
            return CheckResult.failed(f"Pandoc DOCX failed: {e.stderr}")
        except FileNotFoundError:
            return CheckResult.failed("Pandoc not found. Please install pandoc.")


@plugin("bh_mdpi_zip_package")
class MDPISubmissionZipper(BaseCheck):
    """Package DOCX and required figures into a single ZIP for MDPI submission."""

    def _find_repo_root(self, start: pathlib.Path) -> pathlib.Path:
        current = start.resolve()
        for _ in range(8):
            if (current / "logic-graph.yml").exists() or (current / ".git").exists() or (current / "lake-manifest.json").exists():
                return current
            if current.parent == current:
                break
            current = current.parent
        return start.resolve()

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        art_path = pathlib.Path(artifact)
        repo_root = self._find_repo_root(art_path if art_path.exists() else pathlib.Path.cwd())
        artifacts_dir = repo_root / "build" / "artifacts"
        docx_path = artifacts_dir / "article_blackhole_inevitable.docx"

        # Proactively (re)generate required images if missing or stale
        try:
            images_and_scripts = [
                (artifacts_dir / "growth_curves.png", repo_root / "viz" / "generate_plot.py"),
                (artifacts_dir / "robust_recal.png", repo_root / "viz" / "robust_plot.py"),
                (artifacts_dir / "sensitivity_tr.png", repo_root / "viz" / "sensitivity_tr.py"),
                (artifacts_dir / "silence_flow.png", repo_root / "viz" / "silence_flow.py"),
                (artifacts_dir / "info_droplet.png", repo_root / "viz" / "info_droplet.py"),
            ]
            import sys
            for img, script in images_and_scripts:
                try:
                    if (not img.exists()) or (img.stat().st_mtime < script.stat().st_mtime):
                        subprocess.run([sys.executable, str(script)], cwd=str(repo_root), check=True)
                except Exception:
                    pass
        except Exception:
            pass

        required_imgs = [
            artifacts_dir / "growth_curves.png",
            artifacts_dir / "robust_recal.png",
            artifacts_dir / "sensitivity_tr.png",
            artifacts_dir / "silence_flow.png",
            artifacts_dir / "info_droplet.png",
        ]

        missing = [p for p in [docx_path, *required_imgs] if not p.exists()]
        if missing:
            return CheckResult.failed("Missing for MDPI ZIP: " + ", ".join(str(m) for m in missing))

        zip_path = artifacts_dir / "mdpi_submission.zip"

        try:
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                # Main manuscript
                zf.write(docx_path, arcname=docx_path.name)
                # Figures
                for img in required_imgs:
                    zf.write(img, arcname=f"figures/{img.name}")
            return CheckResult.passed(f"MDPI ZIP created: {zip_path}")
        except Exception as e:
            return CheckResult.failed(f"Failed to create MDPI ZIP: {e}")