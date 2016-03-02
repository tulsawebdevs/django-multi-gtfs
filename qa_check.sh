#!/bin/bash
coverage erase
coverage run --source multigtfs ./run_tests.py
if [[ $? -ne 0 ]]; then exit 1; fi
coverage report
flake8 --exclude=".tox" .
