.PHONY: run build

build:
	docker build -t jokes-app:0.1.0 .

run:
	docker run -it --rm --name jokes-app-docker jokes-app:0.1.0

stop:
	@echo "Stopping docker containers"
	docker stop $(shell docker ps -q -a)
