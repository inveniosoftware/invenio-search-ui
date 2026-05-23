#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2015-2022 CERN.
# SPDX-FileCopyrightText: 2022 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

python -m check_manifest
python -m sphinx.cmd.build -qnNW docs docs/_build/html
python -m pytest
tests_exit_code=$?
exit "$tests_exit_code"
