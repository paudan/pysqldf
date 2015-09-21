#!/bin/bash

pandoc -f markdown -t rst README.md > README.rst
python setup.py sdist # check egg and dist files

# test pypi upload
python setup.py register -r https://testpypi.python.org/pypi
python setup.py sdist upload -r https://testpypi.python.org/pypi

# install from test pypi
# pip install --index-url https://testpypi.python.org/simple/ pysqldf

# pypi upload
# python setup.py register
# python setup.py sdist upload
