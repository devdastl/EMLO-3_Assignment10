#makefile to work with dockerfile

#vars
USERNAME = devdastl
PROJECT = emlop
TAG = assignment10-v1

#setup make commands
help:
	@echo "Makefile supported commands:"
	@echo "build-image: Build image from Dockerfile"
	@echo "run-interactive: Run docker container in interactive mode"
	@echo "run-train: Run training on default config"

build-gpt:
	@echo "building docker image for GPT service"
	docker build -f gpt_service/Dockerfile -t ${USERNAME}/${PROJECT}:${TAG}-gpt gpt_service

build-vit:
	@echo "building docker image for VIT service"
	docker build -f vit_service/Dockerfile -t ${USERNAME}/${PROJECT}:${TAG}-vit vit_service

build-images: build-gpt build-vit
	@echo "building both docker images for GPT and VIT service"

pull-images:
	@echo "pulling GPT service image"
	docker pull ${USERNAME}/${PROJECT}:${TAG}-gpt

	@echo "pulling VIT service image"
	docker pull ${USERNAME}/${PROJECT}:${TAG}-vit

run-gpt-service:
	docker run -it -p 8080:8080 ${USERNAME}/${PROJECT}:${TAG}-gpt

run-vit-service:
	docker run -it -p 8080:8080 ${USERNAME}/${PROJECT}:${TAG}-vit

run-gpt-test:
	@echo "running GPT test on port and localhost of EC2"
	python3 gpt_service/test_gpt_service.py

run-vit-test:
	@echo "running VIT test on port 8080 and localhost of EC2"
	python3 vit_service/test_vit_service.py