#!/usr/bin/env sh

python3 setup.py sdist build
twine upload dist/* -r pypi
