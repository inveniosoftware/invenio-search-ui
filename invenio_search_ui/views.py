# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI for Invenio-Search."""

from __future__ import absolute_import, print_function

from copy import deepcopy

from flask import Blueprint, current_app, json, render_template

blueprint = Blueprint(
    "invenio_search_ui",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@blueprint.route("/search")
def search():
    """Search page ui."""
    return render_template(current_app.config["SEARCH_UI_SEARCH_TEMPLATE"])


def sorted_options(sort_options):
    """Sort sort options for display.

    :param sort_options: A dictionary containing the field name as key and
        asc/desc as value.
    :returns: A dictionary with sorting options for Invenio-Search-JS.
    """
    return [
        {
            "title": v["title"],
            "value": (
                "-{0}".format(k)
                if v.get("default_order", "asc") == "desc"
                else k
            ),
        }
        for k, v in sorted(
            sort_options.items(), key=lambda x: x[1].get("order", 0)
        )
    ]


@blueprint.app_template_filter("format_sortoptions")
def format_sortoptions(sort_options):
    """Create sort options JSON dump for Invenio-Search-JS."""
    return json.dumps({"options": sorted_options(sort_options)})


class SearchAppInvenioRestConfigHelper(object):
    """Configuration generator for Invenio-Search-JS.

    Using the existing configuration from Invenio-Records-REST we can
       prefill most of the needed information required for the initialisation
       of SearchApp.
    """

    default_options = dict(
        endpoint_id=None,
        hidden_params=None,
        app_id='search',
        headers=None,
        list_view=True,
        grid_view=True,
        pagination_options=(10, 20, 50),
        default_size=10,
    )

    def __init__(self, configuration_options):
        """Initialize the search configuration.

        :param endpoint_id: The string endpoint ID as used in Records Rest.
        :param hidden_params: Nested arrays containing any additional query
            parameters to be used in the search.
        :param app_id: The string ID of the Search Application.
        :param headers: Dictionary containing additional headers to be included
             in the request.
        :param list_view: Boolean enabling the list view of the results.
        :param grid_view: Boolean enabling the grid view of the results.
        :param pagination_options: An integer array providing the results per
            page options.
        :param default_size: An integer setting the default number of results
            per page.
        """
        options = deepcopy(self.default_options)
        options.update(configuration_options)
        for key, value in options.items():
            setattr(self, key, value)

    @property
    def _rest_config(self):
        """Get endpoint configuration."""
        return current_app.config['RECORDS_REST_ENDPOINTS'][self.endpoint_id]

    @property
    def appId(self):
        """."""
        return self.app_id

    @property
    def initialQuerystate(self):
        """Generate initialQueryState."""
        return {
            'hiddenParams': self.hidden_params,
        }

    @property
    def searchApi(self):
        """Generate searchAPI configuration."""
        headers = {"Accept": self._rest_config["default_media_type"]}
        headers.update(getattr(self, 'additional_headers', {}))
        return {
            "axios": {
                "url": "/api{}".format(self._rest_config["list_route"]),
                "withCredentials": True,
                "headers": headers
            }
        }

    @property
    def layoutOptions(self):
        """Generate the Layout Options.

        :returns: A dict with the options for React-SearchKit JS.
        """
        return {
            'listView': self.list_view,
            'gridView': self.grid_view
        }

    @property
    def sortOptions(self):
        """Format sort options to be used in React-SearchKit JS.

        :returns: A list of dicts with sorting options for React-SearchKit JS.
        """
        search_index = self._rest_config["search_index"]
        sort_options = current_app.config.get(
            "RECORDS_REST_SORT_OPTIONS", {}).get(search_index, {})
        default_sort = current_app.config.get(
            "RECORDS_REST_DEFAULT_SORT", {}).get(search_index, {})

        return [
            {
                "text": v["title"],
                "sortBy": k,
                "sortOrder": v.get("default_order", "asc"),
                "default": default_sort["query"] == k,
                "defaultOnEmptyString": default_sort["noquery"] == k
            }
            for k, v in sorted(
                sort_options.items(), key=lambda x: x[1].get("order", 0)
            )
        ]

    @property
    def aggs(self):
        """Format the aggs configuration to be used in React-SearchKit JS.

        :returns: A list of dicts for React-SearchKit JS.
        """
        search_index = self._rest_config["search_index"]
        aggs = (
            current_app.config.get("RECORDS_REST_FACETS", {})
            .get(search_index, {})
            .get("aggs", {})
        )
        return [
            {
                "title": k.capitalize(),
                "aggName": k,
                "field": v["terms"]["field"]
            }
            for k, v in aggs.items()
        ]

    @property
    def paginationOptions(self):
        """Format the pagination options to be used in React-SearchKit JS.

        :param options: A list of integers.
        :default_size: An integer defining the default option.
        :returns: A list of dicts with the appropriate format
         for React-SearchKit JS.
        """
        if not getattr(self, 'default_size') or \
                self.default_size not in self.pagination_options:
            raise ValueError(
                'Parameter default_size should be part of options')
        return {
                "defaultValue": self.default_size,
                "resultsPerPage": [
                    {"text": str(option), "value": option}
                    for option in self.pagination_options
                ]
            }

    @classmethod
    def generate(cls, options, **kwargs):
        """Create JSON config for Invenio-Search-JS with InvenioREST config."""
        generator_object = cls(options)
        config = {
            "appId": generator_object.appId,
            "initialQueryState": generator_object.initialQuerystate,
            "searchApi": generator_object.searchApi,
            "sortOptions": generator_object.sortOptions,
            "aggs": generator_object.aggs,
            "layoutOptions": generator_object.layoutOptions,
            "paginationOptions": generator_object.paginationOptions

        }
        config.update(kwargs)
        return config


@blueprint.app_context_processor
def search_app_helpers():
    """Makes Invenio-Search-JS config generation available for Jinja."""
    return {
        'search_app_helpers': current_app.config['SEARCH_UI_SEARCH_CONFIG_GEN']
    }
