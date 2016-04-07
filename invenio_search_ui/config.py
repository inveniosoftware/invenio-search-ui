# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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
SEARCH_UI_SEARCH_INDEX = 'records'
SEARCH_UI_SEARCH_TEMPLATE = 'invenio_search_ui/search.html'
SEARCH_UI_JSTEMPLATE_COUNT = 'templates/invenio_search_ui/count.html'
SEARCH_UI_JSTEMPLATE_ERROR = 'templates/invenio_search_ui/error.html'
SEARCH_UI_JSTEMPLATE_FACETS = \
    'node_modules/invenio-search-js/dist/templates/facets.html'
SEARCH_UI_JSTEMPLATE_LOADING = 'templates/invenio_search_ui/loading.html'
SEARCH_UI_JSTEMPLATE_PAGINATION = 'templates/invenio_search_ui/pagination.html'
SEARCH_UI_JSTEMPLATE_RESULTS = \
    'templates/invenio_search_ui/marc21/default.html'
SEARCH_UI_JSTEMPLATE_SELECT_BOX = 'templates/invenio_search_ui/selectbox.html'
SEARCH_UI_JSTEMPLATE_SORT_ORDER = \
    'templates/invenio_search_ui/togglebutton.html'
