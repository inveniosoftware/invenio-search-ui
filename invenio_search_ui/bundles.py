# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
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
        "almond": "~0.3.1",
        'angular': '~1.4.10',
        'angular-loading-bar': '~0.9.0',
        'd3': '^3.5.17',
        'invenio-search-js': '~0.2.0',
    },
)
