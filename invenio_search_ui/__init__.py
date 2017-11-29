# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2017 CERN.
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

"""UI for Invenio-Search.

Invenio-Search-UI is responsible for providing an interactive user interface
for displaying, filtering and navigating search results from the various
endpoints defined in Invenio-Records-REST. This is achieved though the usage of
the Invenio-Search-JS AngularJS package and its configuration inside Jinja and
AngularJS templates.

Although a default ``/search`` endpoint is provided, meant for displaying
search results for the main type of records an Invenio instance is storing, it
is also possible to define and integrate multiple search result pages by
extension and configuration of some base Jinja and AngularJS templates.

Initialization
--------------
First create a Flask application:

>>> from flask import Flask
>>> app = Flask('myapp')
>>> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

There are several dependencies that should be initialized in order to make
Invenio-Search-UI work correctly.

>>> from invenio_db import InvenioDB
>>> from invenio_pidstore import InvenioPIDStore
>>> from invenio_records import InvenioRecords
>>> from invenio_rest import InvenioREST
>>> from invenio_theme import InvenioTheme
>>> from invenio_i18n import InvenioI18N
>>> from invenio_search_ui.bundles import js
>>> InvenioDB(app)
>>> InvenioPIDStore(app)
>>> InvenioRecords(app)
>>> InvenioREST(app)
>>> InvenioTheme(app)
>>> InvenioI18N(app)

Register the JavaScript bundle, containing Invenio-Search-JS

>>> from invenio_assets import InvenioAssets
>>> assets = InvenioAssets(app)
>>> assets.env.register('invenio_search_ui_search_js', js)

>>> from invenio_search import InvenioSearch
>>> from invenio_indexer import InvenioIndexer
>>> InvenioIndexer(app)
>>> search = InvenioSearch(app)
>>> # search.register_mappings('testrecords', 'data')

>>> from invenio_search_ui import InvenioSearchUI
>>> from invenio_search_ui.views import blueprint
>>> InvenioSearchUI(app)
>>> app.register_blueprint(blueprint)

Configuration
~~~~~~~~~~~~~
Before we initialize the InvenioSearchUI extension, we need to configure some
REST API endpoints to expose our records. Let's start with one endpoint
``/records/`` which resolves integer record identifiers to internal record
objects.

>>> from invenio_search.api import RecordsSearch
>>> app.config['RECORDS_REST_ENDPOINTS'] = dict(
...     recid=dict(
...         pid_type='recid',
...         pid_minter='recid',
...         pid_fetcher='recid',
...         search_class=RecordsSearch,
...         search_index='records',
...         record_serializers={
...             'application/json':
...                 'invenio_records_rest.serializers:json_v1_response',
...         },
...         search_serializers={
...             'application/json':
...                 'invenio_records_rest.serializers:json_v1_search',
...         },
...         list_route='/records/',
...         item_route='/records/<pid(recid):pid_value>',
...         default_media_type='application/json',
...     )
... )
>>> from invenio_records_rest import InvenioRecordsREST
>>> from invenio_records_rest.utils import PIDConverter
>>> from invenio_records_rest.facets import range_filter, terms_filter
>>> app.url_map.converters['pid'] = PIDConverter
>>> InvenioRecordsREST(app)

In order for the following examples to work, you need to work within an
Flask application context so let's push one:

>>> ctx = app.app_context()
>>> ctx.push()

Also, for the examples to work we need to create the database and tables (note,
in this example we use an in-memory SQLite database):

>>> from invenio_db import db
>>> db.create_all()

And create the indices on Elasticsearch.

>>> list(search.delete(ignore=[400, 404]))
>>> list(search.create(ignore=[400]))
>>> search.client.indices.refresh()


Building Assets
~~~~~~~~~~~~~~~
In order to render the search results page, you will have to build some of
the Javascript and CSS assets that the page depends on. To do so you will
have to run the following commands:

>>> from invenio_assets import InvenioAssets
>>> from invenio_assets.npm import extract_deps
>>> assets = InvenioAssets(app)
>>> assets.collect.collect()
>>> # TODO: run `invenio npm`, `npm install` and `invenio assets build`


Customizing templates
---------------------
All of the visual aspects of the search results page can be customized
by modifying the templates that are passed to the various Angular directives.
Using the :file:`search.html template <../>`_
The default templates can be found in the `Invenio-Search-JS package
<https://github.com/inveniosoftware/invenio-search-js/tree/master/src/\
invenio-search-js/templates/>`_.
To begin customizing the templates you will first have to place them in a
`static/templates` folder of one of your application's blueptints. Paths to
the HTML templates that are placed there, will be passed as arguments to the
Invenio-Search-JS Angular elements, in order to override the default
templates.

.. code-block::jinja

    ...
    <invenio-search-results
     template="{{ url_for('static', filename='templates/my-custom-results.html') }}">
    </invenio-search-results>
    ...

In a similar fashion we can override what is displayed in case our REST API
request returns an error status code (4xx or 5xx).

In our Jinja template `templates/custom-search.html`:

.. code-block::jinja

    ...
    <invenio-search-error
     template="{{ url_for('static', filename='templates/my-custom-error.html') }}"
     message="{{ _('Search failed.') }}">
    </invenio-search-error>
    ...

In our Angular HTML template `static/templates/my-custom-error.html`:

.. code-block::html

    ...
    <div ng-show='vm.invenioSearchError.name'>
      <div class="alert alert-danger">
        <strong>Error:</strong> {{vm.invenioSearchErrorResults.message || errorMessage }}
        <small><a href="https://myapp.org/help.html"></a></small>
      </div>
    </div>
    ...

In the following example, we customize the `results.html` template to include
a link to the record's actual page using the `ng-href` attribute and the
links defined in the `record.links` object. We also include the creators of
the record by using the `ng-repeat` attribute and the
`records.metadata.creators` list.

In our Jinja template `templates/custom-search.html`:

.. code-block::jinja

    <invenio-search-results
     template="{{ url_for('static', filename='templates/my-custom-results.html') }}">
    </invenio-search-results>

In our Angular HTML template `static/templates/my-custom-results.html`:

.. code-block::html

    <ul>
      <li ng-repeat="record in vm.invenioSearchResults.hits.hits track by $index">
        <a ng-href="record.links.self">
          <h5>{{ record.metadata.title_statement.title }}</h5>
        </a>
        <small ng-repeat="creator in record.metadata.creators">
          {{creator.name}}
        </small>
        <p>{{ record.metadata.summary[0].summary }}</p>
      </li>
    </ul>

Available AngularJS templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  - facets.html
  - loading.html
  - searchBar.html
  - selectBox.html
  - toggleButton.html
"""

from __future__ import absolute_import, print_function

from .ext import InvenioSearchUI
from .version import __version__

__all__ = ('__version__', 'InvenioSearchUI')
