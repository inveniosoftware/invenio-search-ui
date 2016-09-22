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


"""Minimal Flask application example for development.

Installation proccess
---------------------

Run ElastiSearch and RabbitMQ servers.

Create the environment and execute flask:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Run the server:

.. code-block:: console

    $ FLASK_APP=app.py flask run --debugger -p 5000

Visit your favorite browser on `http://localhost:5000/search
<http://localhost:5000/search>`_.

Search for example: `wall`.

To be able to uninstall the example app:

.. code-block:: console

    $ ./app-teardown.sh

"""

from __future__ import absolute_import, print_function

import os
from os.path import dirname, join

import jinja2
from flask import Flask, render_template
from flask_babelex import Babel
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_i18n import InvenioI18N
from invenio_indexer import InvenioIndexer
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.facets import range_filter, terms_filter
from invenio_records_ui import InvenioRecordsUI
from invenio_rest import InvenioREST
from invenio_search import InvenioSearch
from invenio_theme import InvenioTheme

from invenio_search_ui import InvenioSearchUI
from invenio_search_ui.bundles import js
from invenio_search_ui.views import blueprint

# Create Flask application
app = Flask(__name__)

app.config.update(
    CELERY_ALWAYS_EAGER=True,
    CELERY_CACHE_BACKEND='memory',
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND='cache',
    DEBUG=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SEARCH_UI_SEARCH_API='/api/records/',
    SEARCH_UI_BASE_TEMPLATE='invenio_theme/page.html',
    SEARCH_UI_SEARCH_INDEX='testrecords',
    INDEXER_DEFAULT_INDEX='testrecords-testrecord-v1.0.0',
    INDEXER_DEFAULT_DOC_TYPE='testrecord-v1.0.0',
    REST_ENABLE_CORS=True,
    RECORDS_REST_ENDPOINTS=dict(
        recid=dict(
            pid_type='recid',
            pid_minter='recid',
            pid_fetcher='recid',
            search_index='testrecords',
            search_type=None,
            search_factory_imp='invenio_records_rest.query.es_search_factory',
            record_serializers={
                'application/json': ('invenio_records_rest.serializers'
                                     ':json_v1_response'),
            },
            search_serializers={
                'application/json': ('invenio_records_rest.serializers'
                                     ':json_v1_search'),
            },
            list_route='/api/records/',
            item_route='/api/records/<pid_value>',
            default_media_type='application/json'
        ),
    ),
    RECORDS_REST_FACETS=dict(
        testrecords=dict(
            aggs=dict(
                authors=dict(terms=dict(
                    field='added_entry_personal_name.personal_name')),
                languages=dict(terms=dict(
                    field='language_code.language_code_of_text_'
                          'sound_track_or_separate_title')),
                topic=dict(terms=dict(
                    field='subject_added_entry_topical_term.'
                          'topical_term_or_geographic_name_entry_element')),
                years=dict(date_histogram=dict(
                    field='imprint.complete_date',
                    interval='year',
                    format='yyyy')),
            ),
            post_filters=dict(
                authors=terms_filter(
                    'added_entry_personal_name.personal_name'),
                languages=terms_filter(
                    'language_code.language_code_of_text_'
                    'sound_track_or_separate_title'),
                topic=terms_filter(
                    'subject_added_entry_topical_term.'
                    'topical_term_or_geographic_name_entry_element'),
                years=range_filter(
                    'imprint.complete_date',
                    format='yyyy',
                    end_date_math='/y'),
            )
        )
    ),
    RECORDS_REST_SORT_OPTIONS=dict(
        testrecords=dict(
            bestmatch=dict(
                title='Best match',
                fields=['-_score'],
                default_order='asc',
                order=1,
            ),
            controlnumber=dict(
                title='Control number',
                fields=['control_number'],
                default_order='desc',
                order=2,
            )
        )
    ),
    RECORDS_REST_DEFAULT_SORT=dict(
        testrecords=dict(query='bestmatch', noquery='-controlnumber'),
    ),
    RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                      'sqlite:///app.db'),
)

Babel(app)

# Set jinja loader to first grab templates from the app's folder.
app.jinja_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(join(dirname(__file__), 'templates')),
    app.jinja_loader
])

InvenioI18N(app)
InvenioDB(app)
InvenioTheme(app)
InvenioRecords(app)
InvenioRecordsUI(app)
search = InvenioSearch(app)
search.register_mappings('testrecords', 'data')
InvenioSearchUI(app)
InvenioREST(app)
InvenioIndexer(app)
InvenioPIDStore(app)

InvenioRecordsREST(app)

assets = InvenioAssets(app)

# Register assets
assets.env.register('invenio_search_ui_search_js', js)


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def records():
    """Load records."""
    import pkg_resources
    import uuid
    from dojson.contrib.marc21 import marc21
    from dojson.contrib.marc21.utils import create_record, split_blob
    from invenio_pidstore import current_pidstore
    from invenio_records.api import Record

    # pkg resources the demodata
    data_path = pkg_resources.resource_filename(
        'invenio_records', 'data/marc21/bibliographic.xml'
    )
    with open(data_path) as source:
        indexer = RecordIndexer()
        with db.session.begin_nested():
            for index, data in enumerate(split_blob(source.read()), start=1):
                # create uuid
                rec_uuid = uuid.uuid4()
                # do translate
                record = marc21.do(create_record(data))
                # create PID
                current_pidstore.minters['recid'](
                    rec_uuid, record
                )
                # create record
                indexer.index(Record.create(record, id_=rec_uuid))
        db.session.commit()


# register the blueprints
app.register_blueprint(blueprint)


@app.route('/')
def index():
    """Frontpage."""
    return render_template(
        'invenio_theme/page.html',
        title='Invenio-Search-UI Example Application')
