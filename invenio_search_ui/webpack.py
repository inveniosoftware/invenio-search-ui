# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS bundles for search-ui.

You include one of the bundles in a page like the example below (using
``base`` bundle as an example):

 .. code-block:: html

    {{ webpack['base.js']}}

"""

from flask import current_app
from flask_webpackext import WebpackBundle


def search_ui():
    """Create webpack asset endpoint."""
    if current_app.config['SEARCH_UI_JS_FRAMEWORK'] == 'react':
        return WebpackBundle(
            __name__,
            'assets',
            entry={
                'search_ui_app': './js/invenio_react_search_ui/index.js',
            },
            dependencies={
                "axios": "^0.19.0",
                "lodash": "^4.17.15",
                "node-sass": "^4.12.0",
                "qs": "^6.8.0",
                "react": "^16.9.0",
                "react-dom": "^16.9.0",
                "react-redux": "^7.1",
                "react-scripts": "3.1.1",
                "redux": "^4.0.4",
                "redux-thunk": "^2.3.0",
                'react-searchkit': '^0.19.0',
                "semantic-ui-css": "^2.4.1",
                "semantic-ui-react": "^0.88.0"
            })

    else:
        return WebpackBundle(
            __name__,
            'assets',
            entry={
                'search_ui_app': './js/invenio_search_ui/app.js',
                'search_ui_theme': './scss/invenio_search_ui/search.scss',
            },
            dependencies={
                'almond': '~0.3.1',
                'angular': '~1.4.10',
                'angular-loading-bar': '~0.9.0',
                'd3': '^3.5.17',
                'invenio-search-js': '^1.3.1',
                'jquery': '~3.2.1',
            })
