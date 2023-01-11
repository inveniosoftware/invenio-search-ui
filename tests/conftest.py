# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import os
import shutil
import tempfile

import jinja2
import pytest
from flask import Flask
from invenio_assets import InvenioAssets
from invenio_i18n import Babel

from invenio_search_ui import InvenioSearchUI
from invenio_search_ui.views import blueprint


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask("testapp")
    app.config.update(
        TESTING=True,
        SEARCH_UI_SEARCH_API="api",
        BASE_TEMPLATE="invenio_search_ui/base.html",
        HEADER_TEMPLATE="invenio_search_ui/base_header.html",
    )
    Babel(app)
    InvenioAssets(app)
    InvenioSearchUI(app)

    @app.route("/api")
    def api():
        return {}

    app.register_blueprint(blueprint)
    # add extra test templates to the search app blueprint, to fake the
    # existence of `invenio-theme` base templates.
    test_templates_path = os.path.join(os.path.dirname(__file__), "templates")
    enhanced_jinja_loader = jinja2.ChoiceLoader(
        [
            app.jinja_loader,
            jinja2.FileSystemLoader(test_templates_path),
        ]
    )
    # override default app jinja_loader to add the new path
    app.jinja_loader = enhanced_jinja_loader
    return app


@pytest.yield_fixture()
def use_records_rest_config(app):
    """Add temporarily a records rest configuration."""
    app.config.update(_RECORDS_REST_CONFIG)
    yield
    for k in _RECORDS_REST_CONFIG:
        del app.config[k]


_RECORDS_REST_CONFIG = dict(
    RECORDS_REST_ENDPOINTS=dict(
        recid=dict(
            list_route="/myrecords/",
            default_media_type="application/json",
            search_index="myrecords",
        )
    ),
    RECORDS_REST_SORT_OPTIONS=dict(
        myrecords=dict(
            test1=dict(order=2, title="Test 1", default_order="desc"),
            test2=dict(order=1, title="Test 2", default_order="asc"),
        )
    ),
    RECORDS_REST_DEFAULT_SORT=dict(myrecords=dict(query="test2", noquery="test1")),
    RECORDS_REST_FACETS=dict(
        myrecords=dict(aggs=dict(type=dict(terms=dict(field="type"))))
    ),
)
