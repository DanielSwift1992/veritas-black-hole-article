from __future__ import annotations

import pathlib
import subprocess
import tempfile
import re
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
        repo_root = artifact
        article_path = repo_root / "build" / "artifacts" / "article_blackhole_inevitable_clean.md"
        
        if not article_path.exists():
            return CheckResult.failed(f"Article not found: {article_path}")
        
        try:
            # Read markdown
            markdown_content = article_path.read_text(encoding="utf-8")
            
            # Convert to PDF directly with pandoc
            output_dir = repo_root / "build" / "artifacts"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_pdf = output_dir / "article_blackhole_inevitable.pdf"
            
            # Use pandoc to convert directly to PDF
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
                temp_md.write(markdown_content)
                temp_md_path = temp_md.name
            
            try:
                result = subprocess.run([
                    "pandoc",
                    temp_md_path,
                    "-o", str(output_pdf),
                    "--pdf-engine=xelatex",  # Better Unicode support
                    "--table-of-contents",
                    "--number-sections",
                    "-V", "geometry:margin=2.5cm",
                    "-V", "fontsize=12pt",
                    "-V", "mainfont=Times New Roman",
                    "-V", "linestretch=1.2",
                    "-V", "title=Informational Black Holes: The Physical Resolution to the Fermi Paradox",
                    "-V", "author=Daniil Strizhov",
                    "-V", "toc-title=Contents",
                    "-V", "tables=true",  # Better table formatting
                    "-V", "longtable=true",  # Allow tables to break across pages
                    "--metadata", "title=Informational Black Holes: The Physical Resolution to the Fermi Paradox",
                    "--shift-heading-level-by=-1"  # Convert ## to # to avoid all being subsections
                ], capture_output=True, text=True, check=True)
                
                return CheckResult.passed(f"PDF compiled: {output_pdf}")
                
            except subprocess.CalledProcessError as e:
                return CheckResult.failed(f"Pandoc failed: {e.stderr}")
            except FileNotFoundError:
                return CheckResult.failed("Pandoc not found. Please install pandoc and pdflatex.")
            finally:
                pathlib.Path(temp_md_path).unlink(missing_ok=True)
                
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
            
            # Save clean markdown
            output_dir = repo_root / "build" / "artifacts"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            clean_md_path = output_dir / "article_blackhole_inevitable_clean.md"
            clean_md_path.write_text(clean_content, encoding="utf-8")
            
            return CheckResult.passed(f"Clean markdown generated: {clean_md_path}")
            
        except Exception as e:
            return CheckResult.failed(f"Clean markdown generation failed: {e}")