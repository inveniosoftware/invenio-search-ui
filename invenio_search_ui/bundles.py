# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI for Invenio-Search."""

import os

from flask_assets import Bundle
from invenio_assets import AngularGettextFilter, GlobBundle, NpmBundle
from pkg_resources import resource_filename

css = Bundle(
    Bundle(
        'scss/invenio_search_ui/search.scss',
        filters='scss,cleancssurl',
    ),
    Bundle(
        'node_modules/angular-loading-bar/build/loading-bar.css',
        filters='cleancssurl',
    ),
    output='gen/search.%(version)s.css'
)


def catalog(domain):
    """Return glob matching path to tranlated messages for a given domain."""
    return os.path.join(
        resource_filename('invenio_search_ui', 'translations'),
        '*',  # language code
        'LC_MESSAGES',
        '{0}.po'.format(domain),
    )


i18n = GlobBundle(
    catalog('messages-js'),
    filters=AngularGettextFilter(catalog_name='invenioSearchUITranslation'),
    output='gen/translations/invenio-search-ui.js',
)


js = NpmBundle(
    'js/invenio_search_ui/app.js',
    filters='requirejs',
    depends=('node_modules/invenio-search-js/dist/*.js', 'node_modules/d3/*'),
    output='gen/search.%(version)s.js',
    npm={
        'almond': '~0.3.1',
        'angular': '~1.4.10',
        'angular-loading-bar': '~0.9.0',
        'd3': '^3.5.17',
        'invenio-search-js': '^1.3.1',
    },
)
