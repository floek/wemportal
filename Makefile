.PHONY: lint docs

build:
	python -m build
lint:
	pylint wemportal/*py
audit:
	pip-audit -r requirements.txt
clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$|.mypy_cache|.pytest_cache)" | xargs rm -rf
all: lint audit
