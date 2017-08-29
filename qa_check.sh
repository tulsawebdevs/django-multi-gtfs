#!/bin/bash
COVERAGE_COMPAT=${COVERAGE_COMPAT:-0}
if [ "${COVERAGE_COMPAT:-0}" == "0" ]
then
    COVERAGE_OMIT="--omit multigtfs/compat.py"
else
    COVERAGE_OMIT=""
fi

coverage erase
coverage run --source multigtfs ${COVERAGE_OMIT} ./run_tests.py
if [[ $? -ne 0 ]]; then exit 1; fi
coverage report
flake8 .
