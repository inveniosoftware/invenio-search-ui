# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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


"""Minimal Flask application example for development.

Installation proccess
---------------------

First preapare all static files:

.. code-block:: console

   $ npm install -g node-sass clean-css requirejs uglify-js
   $ cd examples
   $ flask -a app.py npm
   $ cd static ; npm install ; cd ..
   $ flask -a app.py collect -v
   $ flask -a app.py assets build

Create demo records

.. code-block:: console

   $ flask -a app.py db init
   $ flask -a app.py db create
   $ flask -a app.py fixtures records

Start the server

.. code-block:: console

   $ flask -a app.py run --debugger --reload

Visit your favorite browser on `http://localhost:5000/search
<http://localhost:5000/search>`_.

"""

from __future__ import absolute_import, print_function

from os.path import dirname, join

import jinja2
from flask import Flask, jsonify, request
from flask_babelex import Babel
from flask_cli import FlaskCLI
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch, Query, current_search_client
from invenio_theme import InvenioTheme

from invenio_search_ui import InvenioSearchUI
from invenio_search_ui.bundles import js
from invenio_search_ui.views import blueprint

# Create Flask application
app = Flask(__name__)

app.config.update(
    CELERY_ALWAYS_EAGER=True,
    CELERY_CACHE_BACKEND="memory",
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND="cache",
    DEBUG=True,
    SEARCH_UI_SEARCH_API='invenio_search_ui.api',
    SEARCH_UI_BASE_TEMPLATE='invenio_theme/page.html',
)

FlaskCLI(app)
Babel(app)

# Set jinja loader to first grab templates from the app's folder.
app.jinja_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(join(dirname(__file__), "templates")),
    app.jinja_loader
 ])

InvenioDB(app)
InvenioTheme(app)
InvenioRecords(app)
InvenioSearch(app)
InvenioSearchUI(app)

assets = InvenioAssets(app)
assets.init_cli(app.cli)

# Register assets
assets.env.register('invenio_search_ui_search_js', js)


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def records():
    """Load records."""
    import pkg_resources
    from invenio_records.api import Record
    from dojson.contrib.marc21 import marc21
    from dojson.contrib.marc21.utils import create_record, split_blob

    # pkg resources the demodata
    data_path = pkg_resources.resource_filename(
        'invenio_records', 'data/marc21/bibliographic.xml'
    )
    with open(data_path) as source:
        with db.session.begin_nested():
            for data in split_blob(source.read()):
                Record.create(marc21.do(create_record(data)))


@blueprint.route('/api', methods=['GET', 'POST'])
def api():
    """Search API for search UI demo.

    .. note::

        WARNING! This search API is just for demo proposes only.

    """
    page = request.values.get('page', 1, type=int)
    size = request.values.get('size', 1, type=int)
    query = Query(request.values.get('q', ''))[(page-1)*size:page*size]
    # dummy facets
    query.body["aggs"] = {
        "by_body": {
            "terms": {
                "field": "summary.summary"
            }
        },
        "by_title": {
            "terms": {
                "field": "title_statement.title"
            }
        }
    }
    response = current_search_client.search(
        index=request.values.get('index', 'records'),
        doc_type=request.values.get('type'),
        body=query.body,
    )
    return jsonify(**response)

# register the blueprints
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
