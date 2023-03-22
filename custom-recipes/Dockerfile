FROM mambaorg/micromamba:1.1.0

RUN micromamba install -y \
  -c conda-forge -n base "python=3.9" \
  boa \
  conda-verify \
  git \
  grayskull \
  openssh

RUN micromamba clean --all --yes
