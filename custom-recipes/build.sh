#!/bin/bash

set -euo pipefail
shopt -s inherit_errexit

conda config --add channels conda-forge
conda config --add channels ./conda-bld
conda index ./conda-bld

export CONDA_BLD_PATH="$PWD/conda-bld"

conda mambabuild --skip-existing --python 3.9 --numpy 1.23 --no-anaconda-upload --use-local ./recipes
