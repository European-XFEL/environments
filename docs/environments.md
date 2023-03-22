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

The main module of interest for Python users will be `mamba`, which will load a python environment with many commonly used packages that we expect will be required for data analysis, as well as our own packages. A full list of software available within an environment is available on the documentation pages for that environment:

{{ ENVIRONMENT_LIST }}

## Working with Mamba (Conda)

!!! warning "Do **not** allow `conda init` to modify shell rc files!"

    As mentioned on the DESY documentation page, **conda init is a bad idea on HPC systems** and should not be used [more information here](https://confluence.desy.de/display/MXW/conda+init).

Instead of having `conda init` commands in your `.bashrc`, you should use the more flexible approach of loading a specific module which runs conda init at load time.

For example, to load the 202301 environment, you can run:

```bash
module load exfel mamba/202301
```

Which will execute the code that `conda init` would execute, and then load that specific environment for you in one command.

!!! info "More Information"

    - [Maxwell Conda Documentation](https://confluence.desy.de/pages/viewpage.action?pageId=242328861#Conda/MambaPython-Workingwithconda/mambaonMaxwell)
    - [Conda Documentation](https://docs.conda.io/en/latest/)

### Creating Your Own Environments

To create a new environment, you can use the `mamba create` command. For example:

```bash
mamba create -n myenv python=3.8
```

This will create a new environment called `myenv` with Python 3.8 installed, which can then be activated with `mamba activate myenv`. From here you can install whatever packages you need.

!!! warning "Do not mix conda and pip"

    Conda and pip **do not** play nicely together. If you install a package with pip, then conda will not be able to manage that package, and the environment will likely become inconsistent and broken. It is recommended to stick to either `mamba` **or** `pip` for installing packages, not both.

    If you need to use both, then make sure to install the pip packages **after all conda packages**.

### Creating Jupyter Kernels for Environments

If you want to use Jupyter with a specific environment, you can create a kernel for it, `ipykernel` is required for this. For example, to create a kernel for `myenv`:

```bash
mamba activate myenv
mamba install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

This will create a kernel called `Python (myenv)` which can be selected in the Jupyter notebook interface.

### Layering Environments - Cloning

If you want to create an environment that is based on another environment, you can use the `--clone` option. For example, if you want to use the environment provided by the DA team at European XFEL, but with a few additional packages or with different versions of packages, then you can do the following:

```bash
module load exfel mamba/202301
mamba create --clone 202301 --name my-202301
```

This will create a new environment called `myenv2` which is identical to `myenv`, but is saved in your own directory. This is useful if you want to have an existing environment as a base, but add/change some of the installed packages.

### Layering Environments - `--system-site-packages`

!!! warning "This is not officially supported by conda"

    These environments have a few drawbacks:

    - This is not an officially supported feature of `conda` environments, it will *probably* work but you may run into issues
    - Changes to the base environment may break the derived environment, e.g. if a package is removed/updated in the base environment, it will change for the derived environment as well, which may break it

If you want to create an environment that is based on another environment, but you do not want to clone the entire environment, you can use the `--system-site-packages` option with python's `venv`. For example, to create a new environment called `myenv2` that is based on `myenv`:

```bash
mamba activate myenv
python3 -m venv --system-site-packages my-light-202301
```

This will create a new environment called `myenv2` which is able to load packages from `myenv`, but can still be changed. Note that this is not a conda environment, it is a python virtual environment, so only `pip` packages can be installed.

## Common Issues

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
