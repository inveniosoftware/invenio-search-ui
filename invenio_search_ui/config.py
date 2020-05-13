# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration for Invenio-Search-UI."""

from __future__ import absolute_import, print_function

APP_THEME = ['semantic-ui', 'bootstrap3']

SEARCH_UI_SEARCH_API = '/api/records/'
"""Configure the search engine endpoint."""

SEARCH_UI_SEARCH_INDEX = 'records'
"""Name of the search index used."""

SEARCH_UI_SEARCH_TEMPLATE = 'invenio_search_ui/search.html'
"""Configure the search page template."""

SEARCH_UI_JSTEMPLATE_COUNT = 'templates/invenio_search_ui/count.html'
"""Configure the count template."""

SEARCH_UI_JSTEMPLATE_ERROR = 'templates/invenio_search_ui/error.html'
"""Configure the error page template."""

SEARCH_UI_JSTEMPLATE_FACETS = 'templates/invenio_search_ui/facets.html'
"""Configure the facets template."""

SEARCH_UI_JSTEMPLATE_RANGE = 'templates/invenio_search_ui/range.html'
"""Configure the range template."""

SEARCH_UI_JSTEMPLATE_RANGE_OPTIONS = {'histogramId': '#year_hist',
                                      'selectionId': '#year_select',
                                      'name': 'years',
                                      'width': 180}
"""Configure the range template options."""

SEARCH_UI_JSTEMPLATE_LOADING = 'templates/invenio_search_ui/loading.html'
"""Configure the loading template."""

SEARCH_UI_JSTEMPLATE_PAGINATION = 'templates/invenio_search_ui/pagination.html'
"""Configure the pagination template."""

SEARCH_UI_JSTEMPLATE_RESULTS = \
    'templates/invenio_search_ui/marc21/default.html'
"""Configure the results template."""

SEARCH_UI_JSTEMPLATE_SELECT_BOX = 'templates/invenio_search_ui/selectbox.html'
"""Configure the select box template."""

SEARCH_UI_JSTEMPLATE_SORT_ORDER = \
    'templates/invenio_search_ui/togglebutton.html'
"""Configure the toggle button template."""
