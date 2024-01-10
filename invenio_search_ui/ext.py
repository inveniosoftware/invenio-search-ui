# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI for Invenio-Search."""

from . import config
from .views import blueprint, search


class InvenioSearchUI(object):
    """Invenio-Search-UI extension."""

    def __init__(self, app=None):
        """Extension initialization.

        :param app: The Flask application.
        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization.

        :param app: The Flask application.
        """
        self.init_config(app)
        app.extensions["invenio-search-ui"] = self

        search_view = app.config.get("SEARCH_UI_SEARCH_VIEW", search)
        blueprint.add_url_rule("/search", "search", view_func=search_view)

    def init_config(self, app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        app.config.setdefault(
            "SEARCH_UI_BASE_TEMPLATE", app.config.get("BASE_TEMPLATE")
        )
        app.config.setdefault(
            "SEARCH_UI_HEADER_TEMPLATE", app.config.get("HEADER_TEMPLATE")
        )

        for k in dir(config):
            if k.startswith("SEARCH_UI_"):
                app.config.setdefault(k, getattr(config, k))
