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

from flask_webpackext import WebpackBundle

search_ui = WebpackBundle(
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
