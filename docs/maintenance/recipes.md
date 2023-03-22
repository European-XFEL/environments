# Custom Recipes

If a package does not already have a Conda recipe and is only available on PyPI or via a repository URL, then a recipe should be made for it to allow for installation into the Conda environments.

Creation of the recipes can be automated via [Grayskull](https://github.com/conda-incubator/grayskull), which will attempt to convert the package setup to a Conda recipe, and implement some basic testing as part of the build phase (check that importing the package works, tests that entry points work), and also run [conda-verify](https://github.com/conda/conda-verify) to check package correctness.

Once a recipe has been created, the package must be built and added to a directory that the relevant environment indexes. This can be done with `conda mambabuild ...` (more info in next section), which will attempt to build the package and execute any tests that are included in the recipe.

If Grayskull fails to create a valid recipe, then the Conda documentation on creating recipes should be checked.

## Creating a Recipe

First, you should load a `mambaforge` base environment, which will provide all the tools required to build recipes. This can be done with `module load exfel mambaforge`.

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
3. Create a gztar sdist - `python3 setup.py sdist --formats=gztar`
4. Run grayskull on the sdist archive - `grayskull pypi ./${PATH_TO_SDIST}`

A full example of this is:

```sh
git clone https://github.com/mhantke/h5writer/
cd h5writer
python3 setup.py sdist --formats=gztar
grayskull pypi ./h5writer-0.8.0
```

## Building the Recipes

Once a new recipe is created, it must be built to create an installable package.

If the Conda installation the package is being built for is new, you will have to tell it to use the build target directory as a channel, so that any packages you have built will be installable.

!!! note inline end

    `BUILD_DIRECTORY` is the directory where the recipes are being built to, this will be a `conda-bld` directory in the Conda installation directory. For example that is `/gpfs/exfel/sw/software/mambaforge/22.11/conda-bld` for the `mambaforge/22.11` instance.

```sh
conda config --env --add channels ${BUILD_DIRECTORY}
conda index ${BUILD_DIRECTORY}
```

As it has better performance, Boa (`mambabuild`) is used for the build process:

```sh
conda mambabuild \
  --skip-existing \  # Do not re-build already built packages
  --python 3.9 \  # Set python version for build
  --numpy 1.23 \  # Set numpy version for build
  --no-anaconda-upload \  # Do not attempt to upload package
  --use-local \  # Use local packages for dependencies
  ${RECIPE_DIRECTORY}  # Directory containing recipes
```

If the build runs successfully, then the package will be placed into the build directory, and it will be installable by the Conda instance as the directory is an indexed channel.

If the build was not successful, then the package should be moved out of the `recipes` directory, and can be added to a `broken` directory while it is being fixed. If this is not done then future builds will fail as they the Conda build process builds **all** recipes in the directory, not just a single package.

!!! warning "Multiple builds may be required"

    If this is the first time you are building a package which has multiple unbuilt dependencies (e.g. if all packages are being re-built for a new installation) then you can expect the build to fail, as the package may attempt to be build before its dependencies are built.

    The easiest way around this is to attempt the build again, as the build process will skip any packages which have already been built. This may need to be done multiple times until all dependencies are built.

## FAQ

### License Missing Errors

If a license could not automatically be determined the license file will be set to `PLEASE_ADD_LICENSE_FILE` and the build will fail. To fix this, you need to add the license file to the recipe directory and add the following to the `meta.yaml` file:

```yaml
about:
  license_file: LICENSE  # Change or delete this line
```

Alternatively, delete the `license_file` line from the `meta.yaml` file.

### Flit Packages

There can be issues with the generation of recipes for packages that use `flit` as the build system. For these you need to edit the `meta.yaml` file and add `flit-core` as a requirement manually.

For example:

```yaml
requirements:
  host:
    - python
    - pip
    - flit-core  # Add this line
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
