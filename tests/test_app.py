# SPDX-FileCopyrightText: 2015-2022 CERN.
# SPDX-License-Identifier: MIT


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
