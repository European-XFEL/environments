# European XFEL Environment Management

This repository contains Conda environment specifications and lock files
defining the environments provided for users at EuXFEL.

All environments contain **only** Conda packages, as installing packages via pip
into a Conda environment leads to inconsistencies.

If a package is not packaged on Conda, then a recipe should be created for it,
either by hand or via a tool like Grayskull.
