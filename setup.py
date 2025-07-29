from setuptools import setup, find_packages

setup(
    name="bh_veritas_plugins",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'veritas_plugins': [
            'bh_python_timeline_check = plugins.bh_veritas_plugins.checks:PythonTimelineCheck',
            'bh_lean_proof_check = plugins.bh_veritas_plugins.checks:LeanProofCheck',
            'growth_curve_png_check = plugins.bh_veritas_plugins.checks:growth_curve_png_check',
            'article_table_check = plugins.bh_veritas_plugins.checks:ArticleTableCheck',
            'centralization_energy_check = plugins.bh_veritas_plugins.checks:CentralizationEnergyCheck',
            'robust_png_check = plugins.bh_veritas_plugins.checks:robust_png_check',
            'droplet_png_check = plugins.bh_veritas_plugins.checks:droplet_png_check',
            'storage_table_check = plugins.bh_veritas_plugins.checks:StorageTableCheck',
        ],
    },
) 