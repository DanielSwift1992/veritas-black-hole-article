"""Bh Veritas plugin package: exposes check implementations on import."""

from importlib import import_module as _imp

# Auto-import checks so that @plugin decorators register them.
_imp(__name__ + '.checks')
