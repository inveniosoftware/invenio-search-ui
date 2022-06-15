# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Module tests."""

from flask import Flask

from invenio_search_ui import InvenioSearchUI


def test_version():
    """Test version import."""
    from invenio_search_ui import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    InvenioSearchUI(app)
    assert "invenio-search-ui" in app.extensions

    app = Flask("testapp")
    ext = InvenioSearchUI()
    assert "invenio-search-ui" not in app.extensions
    ext.init_app(app)
    assert "invenio-search-ui" in app.extensions
