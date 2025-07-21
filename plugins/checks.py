from veritas.vertex.plugin_api import plugin
import subprocess
import re

@plugin
class LocalChecks:
    @staticmethod
    def python_timeline_check(src, dst, edge, bus):
        """Runs the Python script and checks if the output contains the expected timeline."""
        script_path = dst.obj.value.split()[1]
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        if result.returncode != 0:
            bus.add_error(f"Python script failed with code {result.returncode}",
                          data={'stderr': result.stderr})
            return

        # Find the line for φ-growth
        phi_line = next((line for line in result.stdout.split('\n') if 'φ' in line), None)
        if not phi_line:
            bus.add_error("Could not find φ-growth scenario in Python script output.",
                          data={'stdout': result.stdout})
            return

        # Extract the year value
        match = re.search(r'(\d+)\s*$', phi_line)
        if not match:
            bus.add_error("Could not parse the year from the φ-growth line.",
                          data={'line': phi_line})
            return

        actual_year_calc = float(match.group(1))
        expected_years_in_future = edge.meta.get('expected_years', 191)
        expected_year = 2025 + expected_years_in_future

        if not (expected_year - 1 <= actual_year_calc <= expected_year + 1):
             bus.add_error(f"Timeline mismatch: expected year around {expected_year}, got {actual_year_calc}",
                          data={'line': phi_line})

    @staticmethod
    def lean_proof_check(src, dst, edge, bus):
        """Runs `lake build` and checks for the absence of 'sorry'."""
        result = subprocess.run(['lake', 'build'], capture_output=True, text=True)

        if result.returncode != 0:
            bus.add_error("`lake build` failed.", data={'stderr': result.stderr})
            return
        
        if 'sorry' in result.stdout.lower():
             bus.add_error("Lean build contains 'sorry'.",
                          data={'stdout': result.stdout})
        
        if 'axiom' in result.stdout.lower():
            bus.add_warning("Lean build contains 'axiom'.",
                          data={'stdout': result.stdout}) 