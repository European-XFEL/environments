.PHONY: all image sif clean

all: sif

image:
	podman build -t hhg-studio:latest .

sif: image
	podman save hhg-studio:latest -o /tmp/hhg-studio.tar
	singularity build hhg-studio.sif docker-archive:///tmp/hhg-studio.tar

