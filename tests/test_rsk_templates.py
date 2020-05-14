# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the search templates with React-SearchKit/Semantic-UI."""

import json

from flask import render_template_string

from invenio_search_ui.views import format_config


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
    # check if the search app element id exists
    assert 'id="search-ui-app"' in rendered


def test_view(app):
    """Test view."""
    with app.test_request_context():
        _check_template()


def test_format_sortoptions(app):
    """Test default sort option filter."""
    sort_options = dict(
        test1=dict(order=2, title="Test 1", default_order="desc"),
        test2=dict(order=1, title="Test 2", default_order="asc"),
    )
    default_sort = dict(query="test2", noquery="test1")
    facets = dict(aggs=dict(type=dict(terms=dict(field="type"))))

    config = dict(
        RECORDS_REST_ENDPOINTS=dict(
            recid=dict(
                list_route="/myrecords/",
                default_media_type="application/json",
                search_index="myrecords",
            )
        ),
        RECORDS_REST_SORT_OPTIONS=dict(myrecords=sort_options),
        RECORDS_REST_DEFAULT_SORT=dict(myrecords=default_sort),
        RECORDS_REST_FACETS=dict(myrecords=dict(facets)),
    )

    assert format_config(config, "recid") == dict(
        api="/api/myrecords/", mimetype="application/json",
        sort_options=[dict(
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
        )]
    )
