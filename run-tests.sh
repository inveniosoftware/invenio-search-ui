#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

python -m check_manifest --ignore ".*-requirements.txt" && \
python -m sphinx.cmd.build -qnNW docs docs/_build/html && \
python -m pytest
