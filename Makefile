install:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"
	.venv/bin/pre-commit install

check:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

format:
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

test:
	.venv/bin/pytest -v

test-replay:
	.venv/bin/claudep -f tests/fixtures/sample_session.jsonl

build:
	.venv/bin/pip install hatch
	.venv/bin/hatch build

clean:
	rm -rf .venv dist build *.egg-info src/*.egg-info

.PHONY: install check format test test-replay build clean
