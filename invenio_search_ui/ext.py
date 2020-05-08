# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI for Invenio-Search."""

from __future__ import absolute_import, print_function

from . import config
from .views import blueprint


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
        app.register_blueprint(blueprint)
        app.extensions['invenio-search-ui'] = self

    def init_config(self, app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        app.config.setdefault(
            'SEARCH_UI_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE', 'invenio_search_ui/base.html')
        )
        app.config.setdefault(
            'SEARCH_UI_HEADER_TEMPLATE',
            app.config.get('HEADER_TEMPLATE',
                           'invenio_search_ui/base_header.html')
        )
        app.config.setdefault(
            'SEARCH_UI_JS_FRAMEWORK',
            app.config.get('JS_FRAMEWORK',
                           'react')
        )
        if app.config.get('SEARCH_UI_JS_FRAMEWORK') == 'react':
            app.config.setdefault(
                'SEARCH_UI_SEARCH_TEMPLATE',
                app.config.get('SEARCH_TEMPLATE',
                               'invenio_search_ui/react_search.html')
            )
        else:
            app.config.setdefault(
                'SEARCH_UI_SEARCH_TEMPLATE',
                app.config.get('SEARCH_TEMPLATE',
                               'invenio_search_ui/search.html')
            )

        for k in dir(config):
            if k.startswith('SEARCH_UI_'):
                app.config.setdefault(k, getattr(config, k))
