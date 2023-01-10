#!/usr/bin/env sh

rm -rf ./dist
python3 setup.py sdist build
twine upload dist/* -r pypi
pip3 install pysunday --upgrade -i https://pypi.org/simple/
