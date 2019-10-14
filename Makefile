.PHONY: run build

build:
	docker-compose build

run:
	docker-compose up

stop:
	@echo "Stopping docker for jokes app and Flask app"
	docker-compose down

