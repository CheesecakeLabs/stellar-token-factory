DEFAULT_PY_VERSION=3.10
CC=python3.10
DEFAULT_HOST=localhost:8000
MANAGE_PATH=src/manage.py
REQUIREMENTS_PATH=src/config/requirements.txt
DEV_REQUIREMENTS_PATH=src/config/requirements/dev.txt
TEST_REQUIREMENTS_PATH=src/config/requirements/test.txt

.PHONY: build clean test help default
default: test

help:
	@echo "Usage: make [build|serve|start|start-dev|install|install-dev|clean-install|clean-install-dev|test|coverage-test|storybook|build-storybook|lint|format-code]"
	@echo
	@echo 'Usage:'
	@echo '    make run             	Run Django server.'
	@echo '    make install-req     	Install default requirements.'
	@echo '    make install-dev-req 	Install default requirements and dev requirements.'
	@echo '    make install-test-req 	Install default requirements and test requirements.'
	@echo '    make install-venv  		Install python ${DEFAULT_PY_VERSION}'
	@echo '    make collect-static		Collect static files.'
	@echo '    make install-pre-commit	Install pre-commit.'
	@echo '    make clean           	Clean the directory tree.'
	@echo '    make test            	Run tests on the project.'
	@echo '    make coverage-test       Run tests on the project and generates a coverage report.'
	@echo '    make lint			 	Runs the linter checker.'
	@echo '    make lint-fix			Try to fix lint erros.'
	@echo

run: clean
	${CC} ${MANAGE_PATH} runserver ${DEFAULT_HOST}

install-req: 
	${CC} -m pip install -r ${REQUIREMENTS_PATH}

install-dev-req: install-req
	${CC} -m pip install -r ${DEV_REQUIREMENTS_PATH}

install-test-req: install-req
	${CC} -m pip install -r ${TEST_REQUIREMENTS_PATH}

install-venv: 
	python${DEFAULT_PY_VERSION} -m pip install virtualenv
	python${DEFAULT_PY_VERSION} -m virtualenv venv

collect-static:
	${CC} src/manage.py collectstatic

install-pre-commit:
	pre-commit install

clean:
	find . -name "*.pyc" -exec rm -f {} \;

test:
	pytest

coverage-test:
	pytest --cov=./ --cov-report=xml

lint:
	pylint --exit-zero -r y ./src

code-formatter-check:
	black --check ./src

code-formatter-fix:
	black ./src