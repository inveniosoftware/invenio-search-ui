..
    This file is part of Invenio.
    Copyright (C) 2020 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Customizing
===========



Configuring the settings of your Search Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A helper is provided to generate the configuration needed for the
React-Searchkit application.
This configuration contains the following information:

`aggs`: A list of aggregations that will add facets to your search accordingly.

.. code-block:: python

    [
        {
            "aggName": "access_right",
            "field": "access_right",
            "title": "Access Right"
        }
    ]

`appId`: The value here is needed since it will be used internally to
differentiate the resources of multiple apps.
"rdm-search"
`initialQueryState`: This object is used to compose the initial search request
that will be sent to the backend.

.. code-block:: python

    {
        "hiddenParams": null,
        "size": 10
    }

`layoutOptions`: Here we can choose which layouts are going to be enabled
in our search page, if both are present then a layout switcher will also be
present in the UI.

.. code-block:: python

    {
        "gridView": false,
        "listView": true
    }

`paginationOptions`: By changing this object you can increase the available
results per page.

.. code-block:: python

    {
        "defaultValue": 10,
        "resultsPerPage": [
        {
            "text": "10",
            "value": 10
        },
        {
            "text": "20",
            "value": 20
        }]
    }

`searchApi`: The searchApi defines the URL for the list REST API, as well as
any headers that may need to be sent along with the request.

.. code-block:: python

    {
        "axios": {
            "headers": {
                "Accept": "application/vnd.inveniordm.v1+json"
            },
            "url": "/api/records",
            "withCredentials": true
        }
    }

`sortOptions`

.. code-block:: python

    [
        {
        "sortBy": "bestmatch",
        "text": "Best match"
        },
        {
        "sortBy": "newest",
        "text": "Newest"
        }
    ]

This helper needs to be provided with the ID of the endpoint registered in your
`RECORDS_REST_ENDPOINTS` configuration.

.. code-block:: python

    SearchAppInvenioRestConfigHelper.generate(
                {'endpoint_id': 'recid'})

It will then generate a react-searchkit compatible configuration, like the
one mentioned above.
You can provide this configuration to the jinja template via the
search_app_helpers macro.
You can also make adjustments to the default values
(e.g. page size) by providing your own when initialising the helper object.

.. code-block:: python

    SearchAppInvenioRestConfigHelper({'default_size':10}).generate(
                {'endpoint_id': 'recid'})

If a part of the automatically generated configuration doesn't suit your case
you can completely overwite it by supplying the .generate function with the
correct one.
This helper is provided to cover most of the basic cases, but if you feel
that you need to replace many parts of the generated configuration object
you can also remove it and provide the configuration object directly.

.. code-block:: python

    # For instance if you want to disable the facets in the UI despite
    # the aggregations being available in the backend.
    SearchAppInvenioRestConfigHelper({'default_size':10}).generate(
                {'endpoint_id': 'recid'}, {'aggs':[]})

Then just add it to your jinja template rendering the search page:

.. code-block:: html+jinja

    <div data-invenio-search-config='{{
    search_app_helpers.invenio_records_rest.generate(
        dict(
        endpoint_id="recid",
        app_id="search"
        )
    ) | tojson(indent=2) }}'></div>



Configuring the components of your Search Application (via createSearchAppInit)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To render a search page you need 3 elements, a jinja template containing a div
element with the attribute 'data-invenio-search-config' populated with a
react-searchkit configuration, while also importing an initialised SearchApp
from invenio-search-ui.

To do the latter you can create a `index.js` file under the `semamantic-ui/js`
folder and use the `createSearchAppInit` from invenio-search-ui to initialise a
SearchApp.
You can point to this additional file by including it to the `entry` object in
`webpack.py`.

.. code-block:: python

    entry={
        "invenio_search_ui_app": "./js/invenio_search_ui/app.js",
    },

Finally just include the created bundle in your jinja template:

.. code-block:: html+jinja

    {%- block javascript %}
        {{ super() }}
        {{ webpack['invenio_search_ui_app.js'] }}
    {%- endblock javascript %}

When the page is loaded then, the jinja template will load the SearchApp
which will try to find the element containing the `data-invenio-search-config`,
get the configuration and render itself in it.
To override seperate components of react-searchkit, you can create your own and
then provide them when initialising the SearchApp.

.. code-block:: javascript

    import { createSearchAppInit } from "@js/invenio_search_ui";
    import {
    MyNewResultListItem,
    } from "./components";

    const initSearchApp = createSearchAppInit({
    "ResultsList.item": MyNewResultListItem,
    });


Configuring the components of your Search Application (via templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An alternative way is to override the components by creating namespaced
templates.
To do that you will need to provide a template (.jsx) under the templates
folder in the following format templates/(search-app-name)/(component-name):

.. code-block:: console

    templates/
        rdm-search/
            ResultList.element.jsx

The component from this path will then be loaded when the Search application
is initialized.


Reusing a component from a different SearchApp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you would like to reuse a component from a different Search App(that has
been already provided via the template method you can do so by providing its
path as a string in the SearchApp initialization:

.. code-block:: javascript

    import { createSearchAppInit } from "@js/invenio_search_ui";

    const initSearchApp = createSearchAppInit({
    "ResultsList.item": 'rdm-search/ResultList.element.jsx',
    });

