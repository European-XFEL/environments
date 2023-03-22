#!/bin/bash

set -euo pipefail
shopt -s inherit_errexit
 
packages=(
    "calibration-client"
    "cfelpyutils"
    "envmodules"
    "euxfel-bunch-pattern"
    "extra-data"
    "extra-geom"
    "h5glance"
    "hdf5-vds-check"
    "karabo-bridge"
    "metadata-client"
    "pasha"
    "princess"
)

mkdir -p recipes
cd recipes

conda config --add channels conda-forge
conda config --add channels /opt/conda/conda-bld
conda index /opt/conda/conda-bld

for p in ${packages[@]};
do
    if [ ! -d "$p" ]; then
        grayskull pypi --recursive $p
    fi
    conda mambabuild --skip-existing --python 3.9 --numpy 1.23 --no-anaconda-upload -c file:///opt/conda/conda-bld --use-local $PWD
    conda index /opt/conda/conda-bld
    if [ $? -ne 0 ]; then
        read  -n 1 -p "Non-zero exit code, press enter to continu"
    fi
done

