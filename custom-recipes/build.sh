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
    if [ -d "$tmp_shm" ]; then
        echo "Cleaning up temporary directory: $tmp_shm"
        rm -rf "$tmp_shm"
    fi
}

trap cleanup_tmp_shm EXIT

tmp_shm=$(mktemp -d -p /dev/shm boa-XXXX)

conda index ./conda-bld

boa build \
  --skip-existing \
  --croot $tmp_shm \
  --output-folder ./conda-bld \
  --target-platform linux-64 \
  $p

conda index ./conda-bld
