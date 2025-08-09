SHELL := /bin/bash

.PHONY: verify docx pdf

verify:
	veritas check --concurrency=1

docx:
	pandoc build/artifacts/article_blackhole_inevitable_clean.md \
	  -o build/artifacts/article_blackhole_inevitable.docx \
	  --standalone --from=markdown+implicit_figures \
	  --resource-path build/artifacts:. --dpi=300
	@echo -n "DOCX size: "; stat -f%z build/artifacts/article_blackhole_inevitable.docx

pdf:
	# PDF собирается плагином; цель оставлена для наглядности
	@echo "Run 'make verify' to build PDF via Veritas graph"

