docker-build:
	docker build -t mamba-grayskull .

define DOCKER_RUN
docker run --rm -it --workdir=/io \
	-v $(HOME)/.ssh:/home/mambauser/.ssh \
	-v $(CURDIR)/conda-bld:/opt/conda/conda-bld \
	-v $(CURDIR):/io \
	mamba-grayskull
endef

bash:
	$(DOCKER_RUN) /bin/bash

build:
	$(DOCKER_RUN) ./build.sh

