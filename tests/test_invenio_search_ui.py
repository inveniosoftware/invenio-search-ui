# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask, render_template_string

from invenio_search_ui import InvenioSearchUI, bundles


def _check_template():
    """Check template."""
    extended = """
        {% extends 'invenio_search_ui/search.html' %}
        {% block javascript %}{% endblock %}
        {% block css %}{% endblock %}
        {% block page_body %}{{ super() }}{% endblock %}
    """
    rendered = render_template_string(extended)
    # Check if the search elements exist
    assert 'invenio-search-bar' in rendered
    assert 'invenio-search-results' in rendered
    assert 'invenio-search-results-count' in rendered
    assert 'invenio-search-results-loading' in rendered
    assert 'invenio-search-results-pagination' in rendered


def test_version():
    """Test version import."""
    from invenio_search_ui import __version__
    assert __version__


def test_bundles():
    """Test bundles."""
    assert bundles.js
    assert bundles.css


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioSearchUI(app)
    assert 'invenio-search-ui' in app.extensions

    app = Flask('testapp')
    ext = InvenioSearchUI()
    assert 'invenio-search-ui' not in app.extensions
    ext.init_app(app)
    assert 'invenio-search-ui' in app.extensions


def test_view(app):
    """Test view."""
    with app.test_request_context():
        _check_template()
