# Custom Recipes

If a package does not already have a Conda recipe and is only available on PyPI or via a repository URL, then a recipe should be made for it to allow for installation into the Conda environments.

Creation of the recipes can be automated via [Grayskull](https://github.com/conda-incubator/grayskull), which will attempt to convert the package setup to a Conda recipe, and implement some basic testing as part of the build phase (check that importing the package works, tests that entry points work), and also run [`conda-verify`](https://github.com/conda/conda-verify) to check package correctness.

Once a recipe has been created, the package must be built and added to a directory that the relevant environment indexes. This can be done with `conda mambabuild ...` (more info in next section), which will attempt to build the package and execute any tests that are included in the recipe.

If Grayskull fails to create a valid recipe, then the Conda documentation on creating recipes should be checked.

## Bootstrapping a Recipe

First, you should load a `mambaforge` base environment, which will provide all the tools required to build recipes. This can be done with `module load exfel mambaforge`.

!!! info

    If running locally, install the `boa` and `grayskull` packages into your mamba environment with `mamba install -c conda-forge boa grayskull`, or install the environments defined in [`./environments/mambaforge`](https://github.com/European-XFEL/environments/tree/main/environments/mambaforge).

Recipes can be created via the Grayskull CLI:

```bash
grayskull pypi --recursive ${PYPI_NAME_OR_URL}
```

The `--recursive` flag is used to tell Grayskull to generate recipes for any dependencies of the package which are also not in a Conda channel.

Note that the argument can be either:

- The name of the package on PyPI, which **must** contain an `sdist` as those are used to generate the recipes
- The URL to a hosted git repository, with a tag or release. If none is specified it will default to using the `latest` tag, which **must** exist
- The path to a `sdist` archive

### From PyPI With an `sdist`

If the package has releases on PyPI with `sdists`, then grayskull has a good chance of working successfully without any additional work. For example:

```sh
grayskull pypi extra-data
```

Will generate a recipe for the `extra-data` package that can be used without any modifications.

### From a Git Repository (no `sdist`)

However if the package does not have a release with an `sdist` then some additional work has to be done.

In the 'worst case' scenario where a package has no releases or tags, and is not on PyPI with an `sdist`, then you must build the `sdist` manually. To do this:

1. Clone the package
2. Go into the package directory
3. Create an sdist, varies depending on the package tool used (e.g. `python3 setup.py sdist`, `flit/poetry build`, etc...)
4. Run grayskull on the sdist archive - `grayskull pypi $PATH_TO_SDIST`

A full example of this is:

```sh
git clone https://github.com/mhantke/h5writer/
cd h5writer
python3 setup.py sdist --formats=gztar
grayskull pypi ./h5writer-0.8.0
```

## Building the Recipes

Once a new recipe is created, it must be built to create an installable package. A Makefile is provided for ease of use, the Makefile will run the build commands in a container, and builds are done in a temporary shared memory directory to improve performance. Build outputs are stored in the `conda-bld` directory.

You can use the Makefile to build all recipes, or a single recipe:

```sh
# Inside the `custom-recipes` directory
make build  # Build all recipes
make build PKG=extra-data  # Build a single recipe
```

!!! note

    The Makefile has a bit of logic to figure out if it is running on a shared node on Maxwell. If it is then it will run the docker command via `srun` (as docker only works on dedicated nodes, not shared nodes). If it is not then it will just use `docker` directly.

If there are issues during the build then you can troubleshoot the process by running the commands manually:

```sh
# Activate the correct environment when on xsoft@maxwell
module load exfel mambaforge
mamba activate base

# Run the build command
boa build \
  --skip-existing \
  --target-platform linux-64 \
  ./recipes/$PACKAGE  # Optional package name

# Once the build is complete, index the build directory
conda index ./conda-bld
```

## FAQ

### Bumping Versions

If the package source is from a release bundle (e.g. PyPI, GitHub release, the url ends in `.tar.gz`) then bumping up the version means incrementing the number in `context: version:` and updating the `sha256` hash, for example:

```diff
 context:
   name: calibration-client
-  version: 11.0.0
+  version: 11.3.0

 package:
   name: '{{ name|lower }}'
   version: '{{ version }}'

 source:
   url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/calibration_client-{{ version }}.tar.gz
-  sha256: 352279e76060a39097064725ac3a46bd825475da18b9c74207ff159b2c1eaf4b
+  sha256: 9d94df40a60eeaf3363848e6a2ed15c07059828a0e5e4b44afa2151fa1847b85

...
```

Where the new hash can be found by checking the source (PyPI shows the hashes on the '[Download Files](https://pypi.org/project/calibration-client/11.3.0/#files)' tab), or by downloading the source and running `sha256sum` on the file.

### License Missing Errors

If a license could not automatically be determined the license file will be set to `PLEASE_ADD_LICENSE_FILE` and the build will fail. To fix this, you need to add the license file to the recipe directory and add the following to the `meta.yaml` file:

```diff
about:
- license_file: PLEASE_ADD_LICENSE_FILE
+ license_file: LICENSE
```

Alternatively, delete the `license_file` line from the `meta.yaml` file.

### Flit Packages

There can be issues with the generation of recipes for packages that use `flit` as the build system. For these you need to edit the `meta.yaml` file and add `flit-core` as a requirement manually.

For example:

```diff
requirements:
  host:
    - python
    - pip
+   - flit-core
  run:
    - python
```

### Different Package Names on PyPI and Conda

Sometimes you'll run into a package that has a different name on PyPI than on Conda. For example, `pyqt5` is `pyqt` on Conda. Grayskull can deal with these differences, however the `pip check` will fail as the package will require `pyqt5` but only `pyqt` will be installed.

The easiest way to deal with this is to create a patch for the package, changing the name just so that the check can run correctly. For example:

```diff
diff --git a/setup.cfg b/setup.cfg
index b6739660..197afdd9 100644
--- a/setup.cfg
+++ b/setup.cfg
@@ -46,7 +46,7 @@ install_requires =
     pycifrw
     python-dateutil
     pyinstaller
-    pyqt5
+    pyqt
     pyfai
     pyqtgraph
     qtpy
```

Patches can be created by cloning the repository, fixing the file, and then running  `git diff > ${PATCH_NAME}.patch`. This will output a patch file which can be added to the recipe directory for the package.

Then you need to add a `patches` section to the `meta.yaml` file:

```yaml
source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/dioptas-{{ version }}.tar.gz
  sha256: 3ad93487d5576334fc15fb63bdd9a86a1a07dd2ebaf7063b4cb361f49d6b7fd9
  patches:
    - pyqt-requirement.patch  # Add this line
```

Now when the package is built, the patch will be applied, changing the package name to the expected one, and the `pip check` will pass.
