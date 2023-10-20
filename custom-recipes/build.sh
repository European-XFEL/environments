#!/bin/bash

set -euo pipefail
shopt -s inherit_errexit

if [ $# -eq 0 ]; then
  p="./recipes"
elif [ $# -eq 1 ]; then
  p="./recipes/$1"
else
  echo "Usage: $0 [package-name]"
  exit 1
fi

cleanup_tmp_shm() {
  if [ -n "${tmp_shm:-}" ] && [ -d "$tmp_shm" ]; then
    echo "Cleaning up temporary directory: $tmp_shm"
    rm -rf "$tmp_shm"
  fi
}

trap cleanup_tmp_shm EXIT

tmp_shm=""
tmp_shm=$(mktemp -d -p /dev/shm boa-XXXX)

if [ -z "$tmp_shm" ]; then
  echo "Failed to create temporary directory."
  exit 1
fi

conda index ./conda-bld

rm -f ./conda-bld/*/$p-*.tar.bz2

boa build \
  --target-platform=linux-64 \
  --croot=$tmp_shm \
  --output-folder=./conda-bld \
  -m ./conda_build_config.yaml \
  $p

conda index ./conda-bld
