DOCKER_RUN := docker run
DOCKER_RUN_MAXWELL := dockerrun
SRUN := srun --partition exfel --time 10:00:00 --pty

UID := $(shell id -u)

ARGS := --rm -it --workdir=/io \
	-v $(CURDIR):/io \
	-v $(CURDIR)/.pkg-cache:/home/mambauser/.conda/pkgs \
	--tmpfs /dev/shm:rw,nosuid,nodev,exec,size=16g \
	--user $(UID):$(UID) \
	--userns keep-id \
	ghcr.io/european-xfel/environments:main

build:
	mkdir -p conda-bld
	mkdir -p .pkg-cache
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
