from setuptools import setup, find_packages

setup(
    name="bh_veritas_plugins",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'veritas_plugins': [
            'bh_python_timeline_check = plugins.bh_veritas_plugins.checks:PythonTimelineCheck',
            'bh_lean_proof_check = plugins.bh_veritas_plugins.checks:LeanProofCheck',
            'growth_curve_png_check = plugins.bh_veritas_plugins.checks:GrowthCurvePngCheck',
            'article_table_check = plugins.bh_veritas_plugins.checks:ArticleTableCheck',
        ],
    },
) 