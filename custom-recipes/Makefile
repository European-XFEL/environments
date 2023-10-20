DOCKER_RUN := docker run
DOCKER_RUN_MAXWELL := dockerrun
SRUN := srun --partition exfel --time 10:00:00 --pty

ARGS := --rm -it --workdir=/io \
	-v $(HOME)/.ssh:/home/mambauser/.ssh \
	-v $(CURDIR)/conda-bld:/opt/conda/conda-bld \
	-v $(CURDIR):/io \
	--tmpfs /dev/shm:rw,nosuid,nodev,exec,size=16g \
	ghcr.io/european-xfel/environments:main

build:
	mkdir -p conda-bld
	@if command -v dockerrun >/dev/null 2>&1; then \
		$(MAKE) build-max; \
	elif command -v srun --help >/dev/null 2>&1; then \
		$(MAKE) build-srun; \
	else \
		$(MAKE) build-docker; \
	fi

build-docker:
	$(DOCKER_RUN) $(ARGS) ./build.sh $(PKG)

build-srun:
	$(SRUN) $(DOCKER_RUN_MAXWELL) $(ARGS) ./build.sh $(PKG)

build-max:
	$(DOCKER_RUN_MAXWELL) $(ARGS) ./build.sh $(PKG)

shell:
	$(DOCKER_RUN) $(ARGS) /bin/bash
