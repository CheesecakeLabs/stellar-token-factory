#!make

help:
	@echo "Usage:"
	@echo "  DOCKER:"
	@echo "    make docker-run				Starts all Docker containers."
	@echo "    make docker-stop				Stops all Docker containers."
	@echo "    make docker-build			Builds all Docker containers."
	@echo ""
	@echo "    make docker-run-frontend		Starts DHO API Docker containers."
	@echo "    make docker-run-backend		Starts Engineering API Docker containers."
	@echo ""
	@echo "    make docker-stop-frontend	Stop DHO API Docker containers."
	@echo "    make docker-stop-backend		Stop Engineering API Docker containers."
	@echo ""
	@echo "    make docker-build-frontend	Build DHO API Docker containers."
	@echo "    make docker-build-backend	Build Engineering API Docker containers."
	@echo ""

docker-run:
	docker-compose --profile all up -d

docker-stop:
	docker-compose --profile all stop

docker-build:
	docker-compose --profile all up --build -d


docker-run-frontend:
	docker-compose --profile frontend up -d

docker-run-backend:
	docker-compose --profile backend up -d


docker-stop-frontend:
	docker-compose --profile frontend down

docker-stop-backend:
	docker-compose --profile backend down


docker-build-frontend:
	docker-compose --profile frontend build

docker-build-backend:
	docker-compose --profile backend build