# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

r"""UI for Invenio-Search.

Invenio-Search-UI is responsible for providing an interactive user interface
for displaying, filtering and navigating search results from the various
endpoints defined in Invenio-Records-REST. This is achieved through the usage
of the Invenio-Search-JS AngularJS package and its configuration inside Jinja
and AngularJS templates.

Although a default ``/search`` endpoint is provided, meant for displaying
search results for the main type of records an Invenio instance is storing, it
is also possible to define multiple search result pages by extending and
configuring some base Jinja and AngularJS templates.

Initialization
--------------

.. note::

    The following commands can be either run in a Python shell or written to
    a separate ``app.py`` file which can then be run via ``python app.py`` or
    by running ``export FLASK_APP=app.py`` and using the ``flask`` CLI tools.

    To make sure that you have all of the dependencies used installed you
    should also run ``pip install invenio-search-ui[all]`` first.

First create a Flask application:

.. code-block:: python

    from flask import Flask
    app = Flask('myapp')

There are several dependencies that should be initialized in order to make
Invenio-Search-UI work correctly.

.. code-block:: python

    from invenio_db import InvenioDB
    from invenio_pidstore import InvenioPIDStore
    from invenio_records import InvenioRecords
    from invenio_rest import InvenioREST
    from invenio_search import InvenioSearch
    from invenio_indexer import InvenioIndexer
    from invenio_theme import InvenioTheme
    from invenio_i18n import InvenioI18N
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    ext_db = InvenioDB(app)
    ext_pid = InvenioPIDStore(app)
    ext_records = InvenioRecords(app)
    ext_rest = InvenioREST(app)
    ext_theme = InvenioTheme(app)
    ext_i18n = InvenioI18N(app)
    ext_indexer = InvenioIndexer(app)
    ext_search = InvenioSearch(app)

Register the JavaScript bundle, containing Invenio-Search-JS:

.. code-block:: python

    from invenio_assets import InvenioAssets
    ext_assets = InvenioAssets(app)

Before we initialize the Invenio-Search-UI extension, we need to have some
REST API endpoints configured to expose our records. For more detailed
documentation on configuring the records REST API, you can look into
`invenio-records-rest <https://invenio-records-rest.readthedocs.io>`_.

By default Records REST exposes a ``/api/records/`` endpoint, which resolves
integer record identifiers to internal record objects. It uses though a custom
Flask URL converter to resolve this integer to a Persistent Identifier, which
needs to be registered:

.. code-block:: python

    from invenio_records_rest import InvenioRecordsREST
    from invenio_records_rest.utils import PIDConverter
    app.url_map.converters['pid'] = PIDConverter
    ext_records_rest = InvenioRecordsREST(app)

Now we can initialize Invenio-Search-UI and register its blueprint:

.. code-block:: python

    from invenio_search_ui import InvenioSearchUI
    from invenio_search_ui.views import blueprint
    ext_search_ui = InvenioSearchUI(app)
    app.register_blueprint(blueprint)

In order for the following examples to work, you need to work within an
Flask application context so let's push one:

.. code-block:: python

    ctx = app.app_context()
    ctx.push()

Also, for the examples to work we need to create the database and tables (note,
in this example we use an in-memory SQLite database):

.. code-block:: python

    from invenio_db import db
    db.create_all()

Building Assets
~~~~~~~~~~~~~~~
In order to render the search results page, you will have to build the
JavaScript and CSS assets that the page depends on. To do so you will have to
run the following commands:

.. code-block:: console

    $ export FLASK_APP=app.py
    $ flask collect
    $ flask npm
    $ cd static && npm install && cd ..
    $ flask assets build

Record data
~~~~~~~~~~~
Last, but not least, we have to create and index a record:

.. code-block:: python

    from uuid import uuid4
    from invenio_records.api import Record
    from invenio_pidstore.providers.recordid import RecordIdProvider
    from invenio_indexer.api import RecordIndexer
    rec = Record.create({
        'title': 'My title',
        'description': 'My record decription',
        'type': 'article',
        'creators': [{'name': 'Doe, John'}, {'name': 'Roe, Jane'}],
        'status': 'published',
    }, id_=uuid4())
    provider = RecordIdProvider.create(object_type='rec', object_uuid=rec.id)
    db.session.commit()
    RecordIndexer().index_by_id(str(rec.id))

{...}

Feel free to create more records in a similar fashion.

Customizing templates
---------------------

Search components
~~~~~~~~~~~~~~~~~

The building blocks for the search result page are all the
``<invenio-search-...>`` Angular directives defined in InvenioSearchJS. You
can think of them as the UI components of a classic search page. All of the
available directives are listed below (with their default template files):

- **<invenio-search-results>** - The actual result item display (:source:`results.html <invenio_search_ui/static/templates/invenio_search_ui/results.html>`)  # noqa: 501
- **<invenio-search-bar>** - Search input box for queries (:source:`searchbar.html <invenio_search_ui/static/templates/invenio_search_ui/searchbar.html>`)  # noqa: 501
- **<invenio-search-pagination>** - Pagination controls for navigating the search result pages (:source:`pagination.html <invenio_search_ui/static/templates/invenio_search_ui/pagination.html>`)  # noqa: 501
- **<invenio-search-sort-order>** - Sort order of results, i.e. ascending/descending (:source:`togglebutton.html <invenio_search_ui/static/templates/invenio_search_ui/togglebutton.html>`)  # noqa: 501
- **<invenio-search-facets>** - Faceting options for the search results (:source:`facets.html <invenio_search_ui/static/templates/invenio_search_ui/facets.html>`)  # noqa: 501
- **<invenio-search-loading>** - Loading indicator for the REST API request (:source:`loading.html <invenio_search_ui/static/templates/invenio_search_ui/loading.html>`)  # noqa: 501
- **<invenio-search-count>** - The number of search results (:source:`count.html <invenio_search_ui/static/templates/invenio_search_ui/count.html>`)  # noqa: 501
- **<invenio-search-error>** - Errors returned by the REST API, e.g. 4xx or 5xx (:source:`error.html <invenio_search_ui/static/templates/invenio_search_ui/error.html>`)  # noqa: 501
- **<invenio-search-range>** - Date or numeric range filtering (:source:`range.html <invenio_search_ui/static/templates/invenio_search_ui/range.html>`)  # noqa: 501
- **<invenio-search-select-box>** - Select box for further filtering (:source:`selectbox.html <invenio_search_ui/static/templates/invenio_search_ui/selectbox.html>`)  # noqa: 501

Each one of them accepts attributes for configuring their specific behavior.
All of them though accept a ``template`` attribute specifying an Angular
HTML template file which will be used for their rendering, thus defining the
component's visual aspects.

In order for them to function, they need to be placed inside
``<invenio-search>`` tags, which also contain the configuration for the
general search mechanics, like the REST API endpoint for the search results,
HTTP headers for the request, extra querystring parameters, etc. You can read
more about these directives and their parameters in the documentation of
`Invenio-Search-JS <http://inveniosoftware.github.io/invenio-search-js/>`_.

These components are placed and configured inside Jinja templates, where one
has the choice to either override individual pre-existing Jinja blocks or even
completely rearrange the way the componentns are organize in the template.

.. note::

    You can find a full example of this type of configuration and templates in
    :source:`search.html <invenio_search_ui/templates/invenio_search_ui/search.html>`
    and :source:`static/templates <invenio_search_ui/static/templates/invenio_search_ui>`.

Creating a new search page
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create a new search page exclusively for records. For that we'll need to
add a new route to our application that will render our custom search page
Jinja template, ``records-search.html``:

.. code-block:: python

    from flask import render_template

    @app.route('/records-search')
    def my_record_search():
        return render_template('records-search.html')

Then we need to extend :source:`search.html <invenio_search_ui/templates/invenio_search_ui/search.html>`,
inside our new ``templates/records-search.html`` template:

.. code-block:: html+jinja

    {# Contents of templates/records-search.html #}

    {% extends 'invenio_search_ui/search.html' %}

    {# We can also change here the title of the page #}
    {% set title = 'My custom records search' %}
    ...

Next we'll have to configure the ``<invenio-search>`` root directive with our
endpoint and some additional querystring parameters:

.. code-block:: html+jinja
    :emphasize-lines: 4-7

    ...
    {%- block body_inner -%}
    <invenio-search
     search-endpoint="/api/records/"
     search-extra-params="{'type': 'article'}"
     search-hidden-params="{'status': 'published'}"
     search-headers="{'Accept': 'application/json'}"
    >
    {{super()}}
    </invenio-search>
    {%- endblock body_inner -%}
    ...

The URL that will be displayed to the user at the top of the search page will
look something like (note the missing "hidden" parameter ``{'status': 'published'}``):

.. code-block:: console

    https://myapp.org/search?type=article

Our requests to the REST API though will look something like this:

.. code-block:: console

    $ # The hidden parameter
    $ curl -H "Accept: application/json" \
        "https://myapp.org/api/records?status=published&type=article"

Now let's modify what is displayed in case our REST API request returns an
error status code (4xx or 5xx). We do so by creating a new Angular template in
``static/templates/error.html`` and passing it to the ``template`` parameter of
the ``<invenio-search-error>`` directive.

In our Jinja template ``records-search.html``:

.. code-block:: html+jinja
    :emphasize-lines: 4

    ...
    {%- block search_error -%}
    <invenio-search-error
     template="{{ url_for('static', filename='templates/error.html') }}"
     message="{{ _('Search failed.') }}">
    </invenio-search-error>
    {%- endblock search_error -%}
    ...

In our new Angular template ``static/templates/error.html``, we are going
to add a link to some documentation page when a search error occurs:

.. code-block:: html
    :emphasize-lines: 4

    <div ng-show='vm.invenioSearchError.name'>
      <div class="alert alert-danger">
        <strong>Error:</strong> {{vm.invenioSearchErrorResults.message || errorMessage }}
        <small><a href="https://myapp.org/help.html"></a></small>
      </div>
    </div>

Let's modify the way our search result items are displayed. In order to do so
we need to create a ``static/templates/results.html`` template and update the
directive's ``template`` attribute.

In our Jinja template ``records-search.html``:

.. code-block:: html+jinja
    :emphasize-lines: 4

    ...
    {%- block search_results %}
    <invenio-search-results
     template="{{ url_for('static', filename='templates/results.html') }}">
    </invenio-search-results>
    {%- endblock search_results %}

In our Angular template ``static/templates/results.html``, we are going to
display a link to the record's actual page using the ``ng-href`` attribute and
the links defined in the ``record.links`` object. We also display the creators
of the record in a list by using the ``ng-repeat`` attribute and the
``records.metadata.creators`` array field.

.. code-block:: html
    :emphasize-lines: 3,6-8

    <ul>
      <li ng-repeat="record in vm.invenioSearchResults.hits.hits track by $index">
        <a ng-href="record.links.self">
          <h5>{{ record.metadata.title }}</h5>
        </a>
        <ul>
          <li ng-repeat="creator in record.metadata.creators">{{creator.name}}</li>
        </ul>
        <p>{{ record.metadata.description }}</p>
      </li>
    </ul>
"""

from .ext import InvenioSearchUI

__version__ = "2.4.0"

__all__ = ("__version__", "InvenioSearchUI")
