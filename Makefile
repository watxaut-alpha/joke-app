.PHONY: run build

build:
	docker build -t jokes-app:0.1.0 .

run:
	docker run -it --rm --name jokes-app-docker jokes-app:0.1.0

kill:
	@echo "Killing docker-airflow containers"
	docker kill $(shell docker ps -q --filter ancestor=puckel/docker-airflow)

stop:
	@echo "Stopping docker-airflow containers"
	docker stop $(shell docker ps -q -a)
