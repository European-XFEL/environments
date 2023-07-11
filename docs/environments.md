# Environments

Environments can be activated either via the module system or via the conda/mamba activate command. Internally the module system just calls the relevant Conda activate commands for you when you load a module, but some may prefer to directly use the Conda commands.

## Module System

Both the Online Cluster and Maxwell use environment modules for managing multiple software environments.

There are a few must-know commands to use environment modules:

!!! info inline end "More Information"

    - [Official Environment Modules Documentation](https://modules.readthedocs.io/en/latest/).
    - [DESY Page on Maxwell Modules](https://confluence.desy.de/display/CCS/Enabling+Software)

| Command                 | Use                                                    |
| ----------------------- | ------------------------------------------------------ |
| `module avail`          | List the available modules                             |
| `module load $MODULE`   | Load a specific module                                 |
| `module list`           | List currently loaded modules                          |
| `module unload $MODULE` | Unload specific module (may not work for some modules) |

DESY and EuXFEL maintain multiple software environments to facilitate user analysis. For DESY specific modules, check the [Maxwell Software List](https://confluence.desy.de/display/IS/Alphabetical+List+of+Packages) and DESY confluence wiki pages.

EuXFEL maintained modules are in their own scope, which can be activated by running `module load exfel`. Once that command has been run, if you use `module list` you will see that many new modules are now available to load.

The main module of interest for Python users will be `exfel-python`, which will load a python environment with many commonly used packages that we expect will be required for data analysis, as well as our own packages. A full list of software available within an environment is available on the documentation pages for that environment (see a list in the [Environment List](#environment-list) section).

To facilitate reproducibility we create a new environment for every cycle. This way, if you want to use the same software as a previous cycle, or if the current cycle causes issues with your code, you can easily switch to a previous environment.

The current cycle is always available as `exfel-python`, and previous cycles are available as `exfel-python/$CYCLE`, where `$CYCLE` is the cycle number. For example, to load the environment for cycle 202301, you can run:

```bash
module load exfel exfel-python/202301
```

## Using our Python Environments

!!! warning "Do **not** allow `conda init` to modify shell rc files!"

    As mentioned on the DESY documentation page, **conda init is a bad idea on HPC systems** and should not be used [more information here](https://confluence.desy.de/display/MXW/conda+init).

Instead of having `conda init` commands in your `.bashrc`, you should use the more flexible approach of loading a specific module which runs conda init at load time.

For example, to load the our most current environment, you can run:

```bash
module load exfel exfel-python
```

Which will perform the same steps as `conda init` but in a way that is compatible with the module system, and then load that specific environment for you in one command.

!!! info "More Information"

    - [Maxwell Conda Documentation](https://confluence.desy.de/pages/viewpage.action?pageId=2423.9861#Conda/MambaPython-Workingwithconda/mambaonMaxwell)
    - [Conda Documentation](https://docs.conda.io/en/latest/)

## Environment List

The "What's Available" section contains a list of our environments, modules, and recipes (conda packages not available on conda or conda forge). This list is automatically generated based on the contents of the [environments](https://github.com/European-XFEL/environments/tree/main/environments) and [modules](https://github.com/European-XFEL/environments/tree/main/modules) directories in this repository.

Currently available python environments are:

{{ ENVIRONMENT_LIST }}

## Creating Your Own Environments

Our environments are not writeable by users, so you cannot add packages to them. Instead you can create your own environment from scratch, or use one of our environments as a base to start from.

### Creating a New Conda Environment

To create a new environment, you can use the `mamba create` command. For example:

```bash
mamba create -n myenv python=3.9
```

This will create a new environment called `myenv` with Python 3.9 installed, which can then be activated with `mamba activate myenv`. From here you can install whatever packages you need.

!!! warning "Do not mix conda and pip"

    Conda and pip **do not** play nicely together. If you install a package with pip, then conda will not be able to manage that package, and the environment will likely become inconsistent and broken. It is recommended to stick to either `mamba` **or** `pip` for installing packages, not both.

    If you need to use both, then make sure to install the pip packages **after all conda packages**, and to not install additional conda packages after a pip package has been installed.

### Layering Environments - Cloning

!!! info inline end

    As this clones the entire environment it can be a slow operation which consumes a large amount of space. See the following section on "Layering Environments" for an alternative.

If you want to create an environment that is based on another environment, you can use the `--clone` option. For example, if you want to use the environment provided by the DA team at European XFEL, but with a few additional packages or with different versions of packages, then you can do the following:

```bash
module load exfel exfel-python/202301
mamba create --clone 202301 --name my-202301
mamba activate my-202301
mamba install ...
```

This will create a new environment called `my-202301` which is identical to `202301`, but is saved in your own directory. This is useful if you want to have an existing environment as a base, but add/change some of the installed packages.

### Layering Environments - `--system-site-packages`

!!! warning "This is not officially supported by conda"

    These environments have a few drawbacks:

    - This is not an officially supported feature of `conda` environments, it will *probably* work but you may run into issues
    - Changes to the base environment may break the derived environment, e.g. if a package is removed/updated in the base environment, it will change for the derived environment as well, which may break it

If you want to create an environment that is based on another environment, but you do not want to clone the entire environment, you can use the `--system-site-packages` option with python's `venv`. For example, to create a new environment called `myenv2` that is based on `exfel-python`:

```bash
module load exfel exfel-python/202301
python3 -m venv --system-site-packages ./my-202301
source ./my-202301/bin/activate
pip install ...
```

This will create a new environment called `my-202301` which is able to load packages from `202301`, but can still be changed. Note that this is not a conda environment, it is a python virtual environment, so only `pip` packages can be installed.

### Adding Individual Packages to an Environment

!!! warning "Not recommended, may cause inconsistent environments!"

    This approach is not recommended, as it is possible to get an inconsistent environment where your local packages are not compatible with the loaded environment.

If you want to add a package to an existing environment, it's possible to load the environment via `module load exfel exfel-python`, and then run `pip install ...` commands.

This will install the package into your local `~/.local/lib/python3.X/site-packages` directory, any packages in this directory will be importable when you activate the environment.

However, this is **not a recommended approach, as it is possible to get an inconsistent environment** - if you install a package with `pip` you may end up locally installing incompatible packages with the ones in the environment, leading to issues.

If you have done this and are experiencing issues then you can temporarily move the `.../site-packages` directory and see if that solves the issue. If it does then it was caused by some incompatible packages.

## Creating Jupyter Kernels for Environments

If you want to use Jupyter with a specific environment, you can create a kernel for it, `ipykernel` is required for this. For example, to create a kernel for `myenv`:

=== "pip+venv"

    ```shell
    $ source some-env/bin/activate
    $ python3 -m pip install ipykernel
    $ python -m ipykernel install --user --name myenv --display-name "Python (some-env)"
    ```

=== "conda"

    ```shell
    $ mamba activate some-env
    $ mamba install ipykernel
    $ python -m ipykernel install --user --name some-env --display-name "Python (some-env)"
    ```

This will create a kernel called `Python (some-env)` which can be selected in the Jupyter notebook interface.

## FAQ

### Interactive Plotting Issues in Jupyter Notebooks

If you have issues with interactive plotting in Jupyter notebooks it is likely that your environment has has some packages installed which are not compatible with the environment that is serving Jupyter.

As of June 2023 it is recommended to pin the following packages to these versions:

```text
- ipympl=0.7.0
- ipywidgets=7.6.3
- matplotlib=3.4.2
```

### Conda Packages and Environments Filling Home Directory

By default, the package cache and environments are placed in your home directory under `~/.mambaforge/pkgs` and `~/.mambaforge/envs` respectively. If you create a lot of environments then these directories can grow quite large and fill up your home directory quota.

!!! note inline end

    This assumes you have a scratch directory, if you do not then first create it by running `mkdir /gpfs/exfel/data/scratch/$USER`.

To change the location of the package cache and/or the environments, you can prepend some paths to the relevant environment variables for example:

```bash
# Add these to your .bashrc or .zshrc
export CONDA_PKGS_DIRS=/gpfs/exfel/data/scratch/$USER/.conda/pkgs:$CONDA_PKGS_DIRS
export CONDA_ENVS_DIRS=/gpfs/exfel/data/scratch/$USER/.conda/envs:$CONDA_ENVS_DIRS
```

This will place the packages in the GPFS scratch directory. Note that scratch means that this is non-permanent storage, so doing this for just the `CONDA_PKGS_DIRS` variable is safe as that is only a cache of package files and deleting it has no impact, but if you do this for `CONDA_ENVS_DIRS` then you risk the environments being deleted if the scratch directory is cleared.

!!! warning "Scratch may be cleared periodically"

    Scratch may be cleared periodically, this in itself isn't an issue as the packages can easily be re-installed **if you keep a record of the environment files**. However, if you don't keep a record of the environment files, then you will have to attempt to re-create your environments from memory.

Another thing to note is that the environment variables `CONDA_PKGS_DIRS` and `CONDA_ENVS_DIRS` take precedence over values set in `.condarc`.

### Using Module System/Environments with SLURM

One way to use the environment in a SLURM batch script is to activate the relevant module and run whatever commands you would normally run interactively:

```bash
#!/bin/bash
#SBATCH --partition=upex
#SBATCH --time=00:10:00
#SBATCH --nodes=1

unset LD_PRELOAD
source /etc/profile.d/modules.sh  # Enable module commands

module load exfel exfel-python/202301

# Commands here
```

!!! warning "Load the module instead of depending on paths"

    Instead of activating the module you could call the python executable for that environment directly, however this is not recommended as it depends on the paths of the environment, which may change in the future.
