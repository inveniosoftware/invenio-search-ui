# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the search templates with React-SearchKit/Semantic-UI."""

from flask import render_template_string

from invenio_search_ui.views import format_config

_RECORDS_REST_CONFIG = dict(
    RECORDS_REST_ENDPOINTS=dict(
        recid=dict(
            list_route="/myrecords/",
            default_media_type="application/json",
            search_index="myrecords",
        )
    ),
    RECORDS_REST_SORT_OPTIONS=dict(myrecords=dict(
        test1=dict(order=2, title="Test 1", default_order="desc"),
        test2=dict(order=1, title="Test 2", default_order="asc"),
    )),
    RECORDS_REST_DEFAULT_SORT=dict(
        myrecords=dict(query="test2", noquery="test1")),
    RECORDS_REST_FACETS=dict(
        myrecords=dict(
            aggs=dict(type=dict(terms=dict(field="type"))))
    )
)


def _check_template():
    """Check template."""
    extended = """
        {% extends 'semantic-ui/invenio_search_ui/search.html' %}
        {% block javascript %}{% endblock %}
        {% block css %}{% endblock %}
        {% block page_body %}{{ super() }}{% endblock %}
    """
    rendered = render_template_string(extended)
    # check if the header search bar element id exists
    assert 'id="header-search-bar"' in rendered
    # check if the search app config attribute exists
    assert 'data-invenio-search-config' in rendered


def test_view(app):
    """Test view."""
    app.config.update(_RECORDS_REST_CONFIG)
    with app.test_request_context():
        _check_template()
    for k in _RECORDS_REST_CONFIG:
        del app.config[k]


def test_format_sortoptions(app):
    """Test default sort option filter."""
    assert format_config(_RECORDS_REST_CONFIG, "recid") == dict(
        appId='search',
        searchApi={
            'axios': {
                'headers': {'Accept': 'application/json'},
                'url': '/api/myrecords/',
                'withCredentials': True
            }
        },
        initialQueryState={'hiddenParams': None},
        layoutOptions={'gridView': True, 'listView': True},
        sortOptions=[dict(
            text="Test 2",
            sortBy="test2",
            sortOrder="asc",
            default=True,
            defaultOnEmptyString=False
        ), dict(
            text="Test 1",
            sortBy="test1",
            sortOrder="desc",
            default=False,
            defaultOnEmptyString=True
        )],
        aggs=[dict(
            title="Type", aggName="type", field="type"
        )],
        paginationOptions={
            "defaultValue": 10,
            "resultsPerPage": [
                {"text": "10", "value": 10},
                {"text": "20", "value": 20},
                {"text": "50", "value": 50},
            ],
        }
    )
