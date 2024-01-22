# European XFEL Environments [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10548701.svg)](https://doi.org/10.5281/zenodo.10548701)

This documentation covers the use, contents, and management of the software environments provided for users at European XFEL.

To learn more about how to use the environments please see the [Using Environments](./environments.md) page, which covers the [Environment Module System](./environments.md#module-system) system used on Maxwell, how to [Work with our Conda/Mamba Environments](./environments.md#working-with-mamba-conda) as well as how to [Create Your Own Environments](./environments.md#creating-your-own-environments).

Most environments are provided via Mamba (a drop-in replacement for Conda, which has better performance for installations), we aim for these environments to be broadly reproducible in the future and as such you can find a

Lock files are provided to ensure that the environments are reproducible, and to allow users to replicate the environments provided on Maxwell locally.

You can find a list of the environments in the [Environment List](./environments.md#environment-list) section, and by clicking the name of the environment you can see what it provides. Alternatively you can directly view the environment definition files in the [environments directory](https://github.com/European-XFEL/environments/tree/main/environments).

<!-- This repository also contains 'applications', which are environments that are specific to a particular application. A list of the applications provided can be found on the [applications page](TODO) of the documentation, or by looking through the [applications directory](TODO). -->

If you would like to create your own custom environments, then check the [Creating Your Own Environments](./environments.md#creating-your-own-environments) section.

Notes on the management of our environments can be found in the Maintenance section ([Environment Management](./maintenance/environments.md), [Recipe Creation](./maintenance/recipes.md), and [Conda Installations](./maintenance/instances.md)). These are intended for the maintainers of the repository, but may be of interest to users wanting to set up their own environments.
