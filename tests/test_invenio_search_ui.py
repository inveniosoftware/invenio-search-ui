# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Module tests."""

from __future__ import absolute_import, print_function

import json

from flask import Flask, render_template_string

from invenio_search_ui import InvenioSearchUI, bundles
from invenio_search_ui.views import format_sortoptions


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
    assert 'invenio-search' in rendered
    assert 'invenio-search-bar' in rendered
    assert 'invenio-search-results' in rendered
    assert 'invenio-search-count' in rendered
    assert 'invenio-search-loading' in rendered
    assert 'invenio-search-pagination' in rendered
    assert 'invenio-search-range' in rendered


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


def test_format_sortoptions(app):
    """Test default sort option filter."""
    sort_options = dict(
        test1=dict(order=2, title='Test1', default_order='desc'),
        test2=dict(order=1, title='Test2', default_order='asc')
    )
    assert json.loads(format_sortoptions(sort_options)) == dict(options=[
        dict(title='Test2', value='test2'),
        dict(title='Test1', value='-test1'),
    ])

