# Conda Installations

A Conda installation is an actual installation of Conda/Mamba itself, which is
used to create the environments that are provided to users.

!!! warning

    Creating a new Conda installation is very rarely required, and is only done
    if a new major version of Conda is released and an upgrade is not possible.

## Creating a New Conda Installation

Mambaforge is the recommended installation method, instructions for installation
can be found [on the Miniforge
repository](https://github.com/conda-forge/miniforge).

Installations are created in `/gpfs/exfel/sw/software/mambaforge/`, and are
named after the version of Mambaforge that is installed. For example, creating a
installation of version `22.11` would be done as follows:

```sh
wget https://github.com/conda-forge/miniforge/releases/download/22.11.1-4/Mambaforge-22.11.1-4-Linux-x86_64.sh
bash Miniforge3.sh -b -p "/gpfs/exfel/sw/software/mambaforge/22.11"
```

Once the installation has been created, you should add a `mamba-init` file to
the `bin` directory of the installation. This file should contain the conda init
code sourced to activate the installation, for example:

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

!!! warn

    The initialisation code should **not** be added to `xsoft`'s shell files, as
    this will cause the Conda installation to be initialised automatically which
    is not desirable for the environment management account.

Now that the installation has been created and the init file is present, create
a module file for the installation. This should be placed in
`/gpfs/exfel/sw/xfel_modules/mambaforge/` and named after the version:

```text
#%Module 1.0
#
#  Mamba
#
module-whatis  "Activate mambaforge 22.11"

prepend-path    PATH                  /gpfs/exfel/sw/software/mambaforge/22.11/bin
setenv          OPENCL_VENDOR_PATH    /etc/OpenCL/vendors
system          "source /gpfs/exfel/sw/software/mambaforge/22.11/bin/mamba-init"

proc ModulesHelp {} {
    puts stdout     " "
    puts stdout     "Activate mambaforge 22.11"
    puts stdout     " "
}
```

Note that the `system` line is required to activate the Conda installation.

Now running `module load mambaforge/22.11` will activate the installation.

### Required Packages

The Conda installation should only contain the packages required to create and
manage the environments. This means that the `base` environment should only
contain `grayskull`, `conda-lock`, `boa` (`mambabuild`) and `git`.

!!! info

    Git is required as the version on Maxwell is very old and does not support
    some of the commands that Conda/Mamba uses.

You should **not** install any user packages into the `base` environment.

So, with the Conda installation activated, run the following commands:

```sh
mamba env activate base
mamba install -c conda-forge grayskull conda-lock boa git
```
