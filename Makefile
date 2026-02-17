.PHONY: docker-up docker-down docker-restart docker-logs docker-ps

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-restart:
	docker-compose restart

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

help:
	@echo "Available commands:"
	@echo "  make docker-up       - Start Docker containers"
	@echo "  make docker-down     - Stop Docker containers"
	@echo "  make docker-restart  - Restart Docker containers"
	@echo "  make docker-logs     - View Docker logs"
	@echo "  make docker-ps       - Show running containers"
