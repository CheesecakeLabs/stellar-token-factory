#!make


help:
	@echo "Usage: make [build|serve|start|start-dev|install|install-dev|clean-install|clean-install-dev|test|coverage-test|storybook|build-storybook|lint|format-code]"
	@echo ""
	@echo "Usage:"
	@echo "  make build  	        	Builds the frontend for production and copies it to the dist folder"
	@echo "  make serve  	        	Serve static files"
	@echo "  make start  	        	Starts the frontend in production mode"
	@echo "  make start-dev         	Starts the frontend in development mode"
	@echo "  make install         		Installs production dependencies based on package.json"
	@echo "  make install-dev       	Installs development dependencies based on package.json"
	@echo "  make clean-install     	Installs production dependencies based on package-lock.json, cleaning all previous installed dependencies"
	@echo "  make clean-install-dev 	Installs development dependencies based on package-lock.json, cleaning all previous installed dependencies"
	@echo "  make test  	        	Runs the frontend tests"
	@echo "  make coverage-test     	Run tests on the project and generates a coverage report."
	@echo "  make storybook         	Starts the storybook"
	@echo "  make build-storybook   	Builds the storybook"
	@echo "  make lint  	        	Runs the frontend linter"
	@echo "  make format-code       	Formats the frontend code with prettier and fix the code style"
	@echo ""

build:
	npm run build

serve:
	serve -l 8000 -s build

start:
	npm run start

start-dev:
	npm run start:dev

install: package.json
	npm install --production

install-dev: package.json
	npm install

clean-install: package-lock.json
	npm ci --production

clean-install-dev: package-lock.json
	npm ci

test:
	npm run test

coverage-test:
	npm run test -- --coverage

storybook:
	npm run storybook

build-storybook:
	npm run build-storybook

lint:
	npm run lint

format-code:
	npm run prettier
