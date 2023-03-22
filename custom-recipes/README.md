# README

This repository Contains conda recipes for packages which we require in our
environments, but which lack a conda package.

- Creation of the recipes is automated as much as possible via [Grayskull](https://github.com/conda-incubator/grayskull).
- Basic testing is performed as part of the build phase, which imports the
  package, and tests that entry points work.
- [conda-verify](https://github.com/conda/conda-verify) runs automatically to
  check package correctness.

## Packages

- calibration-client
- cfelpyutils
- envmodules *
- euxfel-bunch-pattern
- extra-data
- extra-geom
- extra-hed @ git+ssh://git.xfel.eu/tmichela/EXtra-HED **
- findxfel @ git+ssh://git.xfel.eu/dataAnalysis/findxfel *
- geoAssembler @ git+ssh://git@github.com/European-XFEL/geoAssembler.git
- h5glance *
- hdf5-vds-check *
- htmlgen (required by h5glance)
- karabo-bridge
- karabo-bridge-recorder @ git+ssh://git.xfel.eu/dataAnalysis/karabo-bridge-recorder *
- matplotlib-scalebar
- metadata-client
- metropc @ git+ssh://git.xfel.eu/karaboDevices/metropc.git **
- oauth2-xfel-client (required by metadata-client)
- pasha
- princess *

(\*) these packages use flit as their build system, which was added to the `requirements.host` list.
(\*\*) invalid license file, has to be removed from the generated package.

## Adding Packages

A Dockerfile is provided to make running grayskull easier, when in the docker image the steps are:

1. `cd` to the `recipes` directory
2. `grayrkull pypi --recursive {PACKAGE_NAME/GIT_URL}`
3. `conda mambabuild --skip-existing --python 3.9 --numpy 1.23 --no-anaconda-upload -c file://opt/conda/conda-bld --use-local $PWD`
4. Repeat 1-3 for any other packages
5. Add them to the repo
