# Conda Installations

A Conda installation is an actual installation of Conda/Mamba itself, which is used to create the environments that are provided to users.

!!! warning

    Creating a new Conda installation is very rarely required, and is only done if a new major version of Conda is released and an upgrade is not possible.

## Creating a New Conda Installation

Mambaforge is the recommended installation method, instructions for installation can be found [on the Miniforge repository](https://github.com/conda-forge/miniforge).

Installations are created in `/gpfs/exfel/sw/software/mambaforge/`, and are named after the version of Mambaforge that is installed. For example, creating a installation of version `22.11` would be done as follows:

```sh
wget https://github.com/conda-forge/miniforge/releases/download/22.11.1-4/Mambaforge-22.11.1-4-Linux-x86_64.sh
bash Miniforge3.sh -b -p "/gpfs/exfel/sw/software/mambaforge/22.11"
```

Once the installation has been created, you should add a `mamba-init` file to the `bin` directory of the installation. This file should contain the conda init code sourced to activate the installation, for example:

```sh
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/gpfs/exfel/sw/software/mambaforge/22.11/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/gpfs/exfel/sw/software/mambaforge/22.11/etc/profile.d/conda.sh" ]; then
        . "/gpfs/exfel/sw/software/mambaforge/22.11/etc/profile.d/conda.sh"
    else
        export PATH="/gpfs/exfel/sw/software/mambaforge/22.11/bin:$PATH"
    fi
fi
unset __conda_setup

if [ -f "/gpfs/exfel/sw/software/mambaforge/22.11/etc/profile.d/mamba.sh" ]; then
    . "/gpfs/exfel/sw/software/mambaforge/22.11/etc/profile.d/mamba.sh"
fi
# <<< conda initialize <<<
```

!!! warning "Do **not** allow Conda to initialise automatically on xsoft"

    The initialisation code should **not** be added to `xsoft`'s shell files, as this will cause the Conda installation to be initialised automatically which is not desirable for the environment management account.

Now that the installation has been created and the init file is present, create a module file for the installation. This should be placed in `/gpfs/exfel/sw/xfel_modules/mambaforge/` and named after the version:

```tcl
#%Module 1.0
module-whatis  "Mambaforge 22.11"

proc ModulesHelp {} {
    puts stdout    "Activate mambaforge 22.11"
}

set specialuser xsoft

eval set [array get env USER]

if { [ module-info mode load ] } {
    if {$USER != $specialuser} {
        # Set for all users except xsoft
        append-path    CONDA_PKGS_DIRS "~/.conda/pkgs"
        append-path    CONDA_ENVS_DIRS "~/.conda/envs"
    } else {
        append-path    CONDA_PKGS_DIRS "/gpfs/exfel/data/scratch/xsoft/.conda/pkgs"
    }
    puts stdout    "source /gpfs/exfel/sw/software/mambaforge/22.11/bin/mamba-init;"
} elseif { [module-info mode remove] && ![module-info mode switch3] } {
    puts stderr    "Due to how conda-init works, conda cannot be deactivated through the module system."
}
```

The `xsoft` account is a special case in the activation script, as it is the account performing changes to the environments, so it should not have the `CONDA_PKGS_DIRS` and `CONDA_ENVS_DIRS` environment variables set to its home directory.

Now running `module load mambaforge/22.11` will activate the installation.

### Required Packages

The Conda installation should only contain the packages required to create and manage the environments. This means that the `base` environment should only contain `grayskull`, `conda-lock`, `boa` (`mambabuild`) and `git`.

!!! info

    Git is required as the version on Maxwell is very old and does not support some of the commands that Conda/Mamba uses.

You should **not** install any user packages into the `base` environment.

So, with the Conda installation activated, run the following commands:

```bash
mamba env activate base
mamba install -c conda-forge grayskull conda-lock boa git
```

## Summary

The steps, from start to finish, are:

```bash
# Download the installation script
wget https://github.com/conda-forge/miniforge/releases/download/22.11.1-4/Mambaforge-22.11.1-4-Linux-x86_64.sh -o Miniforge-22.11.sh
# Run it to create a new installation
bash Miniforge3.sh -b -p /gpfs/exfel/sw/software/mambaforge/22.11
# Add mamba-init file to /gpfs/exfel/sw/software/mambaforge/22.11/bin/
# Activate the installation
source /gpfs/exfel/sw/software/mambaforge/22.11/bin/mamba-init
mamba env activate base
# Add required base packages
mamba install -c conda-forge grayskull conda-lock boa git
# Create module file in /gpfs/exfel/sw/xfel_modules/mambaforge/
```
