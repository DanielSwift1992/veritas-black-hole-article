from __future__ import annotations

import csv, json, subprocess, sys, pathlib, re, textwrap, os
from typing import List
from veritas.vertex.plugin_api import plugin, BaseCheck, CheckResult

# Allow override via env; default consolidated artifact directory
BUILD_DIR = pathlib.Path(os.getenv("BH_ARTIFACT_DIR", "build/artifacts"))

@plugin("bh_markdown_fill")
class FillMarkdown(BaseCheck):
    """Generate data files via scripts and inject tables/numbers into Markdown."""

    STORAGE_SCRIPT = ["scripts/storage_simple.py", "--csv"]
    PROBE_SCRIPT   = ["scripts/probe_cost.py", "--csv"]
    YEARS_SCRIPT   = ["scripts/get_phi_years.py", "--json"]
    OPPORTUNITY_SCRIPT = ["scripts/opportunity_bits.py", "--csv"]
    ARTICLE        = pathlib.Path("article_blackhole_inevitable_en.md")

    def run(self, artifact: pathlib.Path, **kw) -> CheckResult:
        repo = artifact
        try:
            BUILD_DIR.mkdir(parents=True, exist_ok=True)
            storage_csv = self._run_script(repo, self.STORAGE_SCRIPT, "storage.csv")
            probe_csv   = self._run_script(repo, self.PROBE_SCRIPT,   "probe.csv")
            years_json  = self._run_script(repo, self.YEARS_SCRIPT,   "years.json")
            opportunity_csv = self._run_script(repo, self.OPPORTUNITY_SCRIPT, "opportunity.csv")
            
            # Calculate all values for substitution
            calc_script = repo / "scripts/calculate_all_values.py"
            subprocess.run([sys.executable, str(calc_script)], check=True)
            
        except Exception as e:
            return CheckResult.failed(f"Failed to run scripts: {e}")

        try:
            md_path = repo / self.ARTICLE
            text = md_path.read_text(encoding="utf-8")
            text = _replace_table(text, "storage_simple", storage_csv)
            text = _replace_table(text, "probe", probe_csv)
            text = _replace_table(text, "opportunity", opportunity_csv)
            years_data = json.loads(years_json)
            phi_row = next((it for it in years_data if it["label"].startswith("φ")), None)
            phi_years = phi_row["years"] if phi_row else 192
            text = text.replace("<!--VALUE:phi-->", f"{phi_years:.1f}")
            
            # Substitute all calculated values using {{VALUE}} tags
            values_file = BUILD_DIR / "calculated_values.json"
            if values_file.exists():
                with open(values_file, 'r') as f:
                    values = json.load(f)
                text = _substitute_values(text, values)
            
            md_path.write_text(text, encoding="utf-8")
            return CheckResult.passed("Markdown refreshed from latest data.")
        except Exception as e:
            return CheckResult.failed(f"Failed to update Markdown: {e}")

    def _run_script(self, repo: pathlib.Path, cmd_parts: List[str], out_name: str) -> str:
        script_path = repo / cmd_parts[0]
        cmd = [sys.executable, str(script_path)] + cmd_parts[1:]
        result = subprocess.check_output(cmd, text=True)
        out_file = BUILD_DIR / out_name
        out_file.write_text(result, encoding="utf-8")
        return result

def _replace_table(md: str, tag: str, csv_text: str) -> str:
    lines = list(csv.reader(csv_text.splitlines()))
    hdr, rows = lines[0], lines[1:]
    col_count = len(hdr)
    bar = "|" + "---|" * col_count
    def to_row(r):
        return "| " + " | ".join(r) + " |"
    table_md = "\n".join([to_row(hdr), bar] + [to_row(r) for r in rows])
    pattern = rf"<!--TABLE:{tag}-->[\s\S]*?<!--END:{tag}-->"
    replacement = f"<!--TABLE:{tag}-->\n{table_md}\n<!--END:{tag}-->"
    return re.sub(pattern, replacement, md)

def _substitute_values(text: str, values: dict) -> str:
    """Substitute all <!--VALUE:name--> tags in text"""
    
    def format_value(value, format_type=None):
        if format_type is None:
            return str(value)
        
        if isinstance(value, str):
            return value
        
        if format_type == "int":
            return str(int(value))
        elif format_type == "year":
            return str(int(value))
        elif format_type == "float1":
            return f"{value:.1f}"
        elif format_type == "float2":
            return f"{value:.2f}"
        elif format_type == "float3":
            return f"{value:.3f}"
        elif format_type == "float4":
            return f"{value:.4f}"
        elif format_type == "sci":
            return f"{value:.1e}"
        elif format_type == "big":
            if value >= 1e6:
                return f"{value:,.0f}"
            else:
                return str(int(value))
        elif format_type == "currency":
            if value >= 1:
                return f"{value:.2f}"
            elif value >= 1e-9:
                return f"{value:.10f}".rstrip('0').rstrip('.')
            else:
                return f"~{value:.0e}"
        else:
            return str(value)
    
    def replace_tag(match):
        start_tag = match.group(0).split('-->')[0] + '-->'  # <!--VALUE:name-->
        end_tag = '<!--END:' + match.group(1).split(':')[0] + '-->'  # <!--END:name-->
        tag_content = match.group(1)
        old_value = match.group(2)
        
        # Parse format if specified
        if ':' in tag_content:
            value_name, format_type = tag_content.split(':', 1)
        else:
            value_name = tag_content
            format_type = None
        
        # Get value
        if value_name not in values:
            return start_tag + old_value + end_tag  # Keep original if not found
        
        value = values[value_name]
        formatted_value = format_value(value, format_type)
        return start_tag + formatted_value + end_tag
    
    # Replace all <!--VALUE:name-->old_value<!--END:name--> tags
    pattern = r'<!--VALUE:([^>]+)-->([^<]*)<!--END:[^>]+-->'
    return re.sub(pattern, replace_tag, text)
