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

from invenio_assets.webpack import WebpackThemeBundle

search_ui = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio_search_ui_app": "./js/invenio_search_ui/app.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "@semantic-ui-react/css-patch": "^1.0.0",
                "axios": "^0.21.0",
                "lodash": "^4.17.0",
                "qs": "^6.8.0",
                "react": "^16.13.0",
                "react-dom": "^16.13.0",
                "react-overridable": "^0.0.3",
                "react-redux": "^7.2.0",
                "redux": "^4.0.0",
                "redux-thunk": "^2.3.0",
                "react-searchkit": "^2.0.0",
                "react-invenio-forms": "^1.0.0",
                "semantic-ui-css": "^2.4.0",
                "semantic-ui-react": "^2.1.0",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "react-i18next": "^11.11.0",
            },
            aliases={
                "@js/invenio_search_ui": "js/invenio_search_ui",
                "@translations/invenio_search_ui": "translations/invenio_search_ui",
            },
        ),
        "bootstrap3": dict(
            entry={
                "search_ui_app": "./js/invenio_search_ui/app.js",
                "search_ui_theme": "./scss/invenio_search_ui/search.scss",
            },
            dependencies={
                "almond": "~0.3.1",
                "angular": "~1.4.10",
                "angular-loading-bar": "~0.9.0",
                "d3": "^3.5.17",
                "invenio-search-js": "^1.3.1",
                "jquery": "~3.2.1",
            },
        ),
    },
)
