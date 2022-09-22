DEFAULT_PY_VERSION=3.10
CC=python
DOCKER_COMPOSE=docker-compose
DEFAULT_HOST=localhost:8000
MANAGE_PATH=src/manage.py
REQUIREMENTS_PATH=src/config/requirements.txt
DEV_REQUIREMENTS_PATH=src/config/requirements/dev.txt
TEST_REQUIREMENTS_PATH=src/config/requirements/test.txt

# If the first argument is "docker-up"...
ifeq (docker-up,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: build clean test help default
default: test

help:
	@echo "Usage: make [build|serve|start|start-dev|install|install-dev|clean-install|clean-install-dev|docker-up|test|coverage-test|storybook|build-storybook|lint|format-code]"
	@echo
	@echo 'Usage:'
	@echo '    make run             	Run Django server.'
	@echo '    make docker-up       	Run docker with RUN_ARGS or all by default.'
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

docker-up: 
	${DOCKER_COMPOSE} up --build $(RUN_ARGS)

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
	black --check ./src

lint-fix:
	black ./src