help:
	@echo "Targets:"
	@echo "    make setuptools"
	@echo "    make install"
	@echo "    make test"
	@echo "    make build"
	@echo "    make lint"
	@echo "    make publish"
	@echo "    make bumpversion-major"
	@echo "    make bumpversion-minor"
	@echo "    make bumpversion-patch"
	@echo "    make clean"
	@echo "    make clean-test"

lint:
	pre-commit run --all-files

test:
	pytest

bumpversion-major:
	bumpversion major --allow-dirty

bumpversion-minor:
	bumpversion minor

bumpversion-patch:
	bumpversion patch

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
