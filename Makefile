.PHONY: run dev

run:
	python -c "import run; run.run();"

dev:
	python -c "import run; run.devrun()"