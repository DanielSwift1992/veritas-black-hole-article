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
            'probe_table_check = plugins.bh_veritas_plugins.checks:ProbeTableCheck',
            'bh_pandoc_check = plugins.bh_veritas_plugins.latex_compiler:PandocCheck',
            'bh_latex_pdf_compile = plugins.bh_veritas_plugins.latex_compiler:LaTeXPDFCompiler',
            'bh_clean_markdown_compile = plugins.bh_veritas_plugins.latex_compiler:CleanMarkdownCompiler',
            'bh_markdown_fill = plugins.bh_veritas_plugins.fill_markdown:FillMarkdown',
            'bh_cleanup_artifacts = plugins.bh_veritas_plugins.cleanup:CleanupArtifacts',
            'bh_generate_growth_plot = plugins.bh_veritas_plugins.visualizations:GenerateGrowthPlot',
            'bh_generate_robust_plot = plugins.bh_veritas_plugins.visualizations:GenerateRobustPlot',
            'bh_generate_droplet_plot = plugins.bh_veritas_plugins.visualizations:GenerateDropletPlot',
            'bh_generate_silence_flow = plugins.bh_veritas_plugins.visualizations:GenerateSilenceFlow',
            'values_resolved_check = plugins.bh_veritas_plugins.checks:ValuesResolvedCheck',
            'clean_markdown_no_tags_check = plugins.bh_veritas_plugins.checks:CleanMarkdownNoTagsCheck',
            'storage_simple_content_check = plugins.bh_veritas_plugins.checks:StorageSimpleContentCheck',
            'values_consistency_check = plugins.bh_veritas_plugins.checks:ValuesConsistencyCheck',
        ],
    },
) 