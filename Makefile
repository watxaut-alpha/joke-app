.PHONY: run build

build:
	docker build -t jokes-app:0.3.0 .

run:
	docker run -it --rm --name jokes-app-docker jokes-app:0.3.0

stop:
	@echo "Stopping docker for jokes app"
	docker stop jokes-app-docker

