#!/bin/bash

# Required due to pyqt package naming difference between PyPI and Conda
# Could not be done as patch file as the line endings are not stable/consistent
sed -i 's/pyqt5/pyqt/' ./setup.cfg

$PYTHON -m pip install . -vv
