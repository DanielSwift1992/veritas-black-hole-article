"""Bh Veritas plugin package: expose all plugin implementations on import.

Importing submodules ensures that @plugin-decorated classes register their
obligations even when the package is used via a local path in logic-graph.yml.
"""

from importlib import import_module as _imp

for _mod in (
    'checks',
    'cleanup',
    'latex_compiler',
    'visualizations',
    'fill_markdown',
):
    try:
        _imp(__name__ + '.' + _mod)
    except Exception:
        # Keep import robust; some optional modules may be absent in CI
        pass
