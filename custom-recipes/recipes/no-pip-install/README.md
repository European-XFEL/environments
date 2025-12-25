# No Pip Install

This 'package' use [PEP 668](https://peps.python.org/pep-0668/) to mark a conda environment it is installed into as 'externally managed', disallowing `pip install` commands from being run in the environment.

It should be included in our per-cycle conda environments to prevent the environments from becoming difficult to maintain and track due to changes made by pip.
