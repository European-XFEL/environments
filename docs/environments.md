# Environments

Environments can be activated either via the module system or via the
conda/mamba activate command. Internally the module system just calls the
relevant Conda activate commands for you when you load a module, but some may
prefer to directly use the Conda commands.

## Module System

Both the Online Cluster and Maxwell use environment modules for managing
multiple software environments.

There are a few must-know commands to use environment modules:

!!! info inline end "More Information"

    - [Official Environment Modules Documentation](https://modules.readthedocs.io/en/latest/).
    - [DESY Page on Maxwell Modules](https://confluence.desy.de/display/CCS/Enabling+Software)

| Command | Use |
|---------|-----|
| `module avail` | List the available modules |
| `module load $MODULE` | Load a specific module |
| `module list` | List currently loaded modules |
| `module unload $MODULE` | Unload specific module (may not work for some modules) |

Both DESY and EuXFEL maintain multiple software environments to facilitate user
analysis. For DESY specific modules, check the [Maxwell Software
List](https://confluence.desy.de/display/IS/Alphabetical+List+of+Packages) and
DESY confluence wiki pages.

EuXFEL maintained modules are in their own scope, which can be activated by running
`module load exfel`. Once that command has been run, if you use `module list` you will
see that many new modules are now available to load.

The main module of interest for Python users will be `mamba`, which will load a
python environment with many commonly used packages that we expect will be
required for data analysis, as well as our own packages. A full list of software
available within an environment is available on the documentation pages for that
environment:

{{ ENVIRONMENT_LIST }}

## Working with Conda

!!! warning "Do **not** allow `conda init` to modify shell rc files!"

    As mentioned on the DESY documentation page, **conda init is a bad idea on HPC
    systems** and should not be used [more information
    here](https://confluence.desy.de/display/MXW/conda+init).

Instead of having `conda init` commands in your `.bashrc`, you should use the
more flexible approach of loading a specific module which runs conda init at
load time.

For example, to load the 202301 environment, you can run:

```bash
module load exfel mamba/202301
```

Which will execute the code that `conda init` would execute, and then load that
specific environment for you in one command.

!!! info "More Information"

    - [Maxwell Conda Documentation](https://confluence.desy.de/pages/viewpage.action?pageId=242328861#Conda/MambaPython-Workingwithconda/mambaonMaxwell)
    - [Conda Documentation](https://docs.conda.io/en/latest/)

