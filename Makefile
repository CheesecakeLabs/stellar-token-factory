#!make

help:
	@echo "Usage:"
	@echo "  DOCKER:"
	@echo "    make docker-run						Starts all Docker containers."
	@echo "    make docker-stop						Stops all Docker containers."
	@echo "    make docker-build					Builds all Docker containers."
	@echo ""		
	@echo "    make docker-run-frontend				Starts Frontend Docker container."
	@echo "    make docker-run-stellar-payments		Starts Stellar Payments Docker container."
	@echo "    make docker-run-backend				Starts Backend Docker container."
	@echo ""		
	@echo "    make docker-stop-frontend			Stop Frontend Docker container."
	@echo "    make docker-stop-stellar-payments	Stop Stellar Payments Docker container."
	@echo "    make docker-stop-backend				Stop Backend Docker container."
	@echo ""		
	@echo "    make docker-build-frontend			Build Frontend Docker container."
	@echo "    make docker-build-stellar-payments	Build Stellar Payments Docker container."
	@echo "    make docker-build-backend			Build Backend Docker container."
	@echo ""

docker-run:
	docker-compose --profile all up -d

docker-stop:
	docker-compose --profile all stop

docker-build:
	docker-compose --profile all up --build -d


docker-run-frontend:
	docker-compose --profile frontend up -d

docker-run-stellar-payments:
	docker-compose --profile stellar-payments up -d

docker-run-backend:
	docker-compose --profile backend up -d


docker-stop-frontend:
	docker-compose --profile frontend down

docker-stop-stellar-payments:
	docker-compose --profile stellar-payments down

docker-stop-backend:
	docker-compose --profile backend down


docker-build-frontend:
	docker-compose --profile frontend build

docker-build-stellar-payments:
	docker-compose --profile stellar-payments build

docker-build-backend:
	docker-compose --profile backend build