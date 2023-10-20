FROM mambaorg/micromamba:1.5.1

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba install -y \
  -n "base" \
  -c conda-forge \
  boa \
  conda-verify \
  git \
  grayskull \
  openssh \
  vim

RUN conda config --system --set channel_priority 'strict'
RUN conda config --system --prepend channels conda-forge
RUN conda config --system --prepend channels nodefaults

RUN micromamba clean --all --yes
