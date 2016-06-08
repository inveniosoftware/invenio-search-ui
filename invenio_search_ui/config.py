# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Configuration for Invenio-Search-UI."""

from __future__ import absolute_import, print_function

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

SEARCH_UI_JSTEMPLATE_FACETS = \
    'node_modules/invenio-search-js/dist/templates/facets.html'
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
