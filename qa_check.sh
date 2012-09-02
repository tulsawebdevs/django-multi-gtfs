#!/bin/bash
./run_tests.py --with-coverage
if [[ $? -ne 0 ]]; then exit 1; fi
pep8 .
pyflakes .
