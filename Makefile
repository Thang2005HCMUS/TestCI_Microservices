.PHONY: help install lint test test-all run-all

SERVICE ?= user-service

help:
	@echo "Targets:"
	@echo "  install        Install shared requirements"
	@echo "  lint           Ruff lint all services"
	@echo "  test           Run tests for SERVICE (default: user-service)"
	@echo "  test-all       Run tests for ALL services"
	@echo "  run-all        Start all services (background)"

install:
	pip install -r requirements.txt

lint:
	ruff check services/

test:
	pytest services/$(SERVICE)/tests/ -v

test-all:
	pytest services/ -v --tb=short

run-all:
	@for svc in user-service product-service order-service notification-service; do \
		uvicorn services.$$svc.app.main:app --port $$(shuf -i 8001-8100 -n1) & \
	done
