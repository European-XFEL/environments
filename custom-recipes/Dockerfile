FROM mambaorg/micromamba:latest

# See: https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#changing-the-user-id-or-name
ARG NEW_MAMBA_USER=mambauser
ARG NEW_MAMBA_USER_ID=1000
ARG NEW_MAMBA_USER_GID=1000

USER root

RUN if grep -q '^ID=alpine$' /etc/os-release; then \
      # alpine does not have usermod/groupmod
      apk add --no-cache --virtual temp-packages shadow=4.13-r0; \
    fi && \
    usermod "--login=${NEW_MAMBA_USER}" "--home=/home/${NEW_MAMBA_USER}" \
        --move-home "-u ${NEW_MAMBA_USER_ID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NEW_MAMBA_USER}" \
        "-g ${NEW_MAMBA_USER_GID}" "${MAMBA_USER}" && \
    if grep -q '^ID=alpine$' /etc/os-release; then \
      # remove the packages that were only needed for usermod/groupmod
      apk del temp-packages; \
    fi && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NEW_MAMBA_USER}" > "/etc/arg_mamba_user" && \
    :

ENV MAMBA_USER=$NEW_MAMBA_USER

USER $MAMBA_USER

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba install -y \
  -n "base" \
  -c conda-forge \
  boa \
  conda-verify \
  git \
  grayskull \
  openssh

RUN conda config --set channel_priority 'strict'
RUN conda config --prepend channels conda-forge
RUN conda config --prepend channels nodefaults

RUN micromamba clean --all --yes
