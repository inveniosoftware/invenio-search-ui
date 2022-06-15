# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the search templates with React-SearchKit/Semantic-UI."""

from flask import render_template_string

from invenio_search_ui.views import SearchAppInvenioRestConfigHelper


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
    assert "data-invenio-search-config" in rendered


def test_view(app, use_records_rest_config):
    """Test view."""
    with app.test_request_context():
        _check_template()


def test_format_sortoptions(app, use_records_rest_config):
    """Test default sort option filter."""
    with app.test_request_context():
        assert SearchAppInvenioRestConfigHelper.generate(
            {"endpoint_id": "recid"}
        ) == dict(
            appId="search",
            searchApi={
                "axios": {
                    "headers": {"Accept": "application/json"},
                    "url": "/api/myrecords/",
                    "withCredentials": True,
                }
            },
            initialQueryState={
                "hiddenParams": None,
                "layout": "list",
                "page": 1,
                "size": 10,
                "sortBy": "test2",
                "sortOrder": "asc",
            },
            layoutOptions={"gridView": True, "listView": True},
            sortOptions=[
                dict(
                    text="Test 2",
                    sortBy="test2",
                    sortOrder="asc",
                ),
                dict(
                    text="Test 1",
                    sortBy="test1",
                    sortOrder="desc",
                ),
            ],
            aggs=[dict(title="Type", agg=dict(aggName="type", field="type"))],
            paginationOptions={
                "resultsPerPage": [
                    {"text": "10", "value": 10},
                    {"text": "20", "value": 20},
                    {"text": "50", "value": 50},
                ],
            },
            defaultSortingOnEmptyQueryString={"sortBy": "test1", "sortOrder": "desc"},
        )
