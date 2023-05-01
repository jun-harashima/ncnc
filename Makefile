export PROJECT_NAME=ncnc
export IMAGE_NAME=$(PROJECT_NAME)-image
export CONTAINER_NAME=$(PROJECT_NAME)-container
export PWD=$(shell pwd)

docker-build:
	docker build -t $(IMAGE_NAME) -f Dockerfile .

docker-run:
	docker run -it --rm -v $(PWD):/work --name $(CONTAINER_NAME) $(IMAGE_NAME)

remove-image:
	docker rmi -f $(IMAGE_NAME)

remove-container:
	docker rm -f $(CONTAINER_NAME)

pytest:
	env PYTHONPATH=. poetry run pytest -vv

pysen-lint:
	poetry run pysen run lint

pysen-format:
	poetry run pysen run format
