# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Search app configuration helper."""

from copy import deepcopy

from flask import current_app


class SearchOptionsSelector:
    """Generic helper to select and validate facet/sort options."""

    def __init__(self, available_options, selected_options):
        """Initialize selector."""
        self.available_options = available_options
        self.selected_options = selected_options

    def __iter__(self):
        """Iterate over options to produce RSK options."""
        for o in self.selected_options:
            yield self.map_option(o, self.available_options[o])

    def map_option(self, key, option):
        """Map an option."""
        return (key, option)


class SortConfig(SearchOptionsSelector):
    """Sort options for the search configuration."""

    def __init__(
        self, available_options, selected_options, default=None, default_no_query=None
    ):
        """Initialize sort options."""
        super().__init__(available_options, selected_options)

        self.default = selected_options[0] if default is None else default
        self.default_no_query = (
            selected_options[1] if default_no_query is None else default_no_query
        )

    def map_option(self, key, option):
        """Generate a RSK search option."""
        return {"sortBy": key, "text": option["title"]}


class FacetsConfig(SearchOptionsSelector):
    """Facets options for the search configuration."""

    def map_option(self, key, option):
        """Generate an RSK aggregation option."""
        title = option.get("title", option["facet"]._label)

        ui = deepcopy(option["ui"])
        ui.update(
            {
                "aggName": key,
                "title": title,
            }
        )

        # Nested facets
        if "childAgg" in ui:
            ui["childAgg"].setdefault("aggName", "inner")
            ui["childAgg"].setdefault("title", title)

        return ui


class SearchAppConfig:
    """Configuration generator for React-SearchKit."""

    default_options = dict(
        endpoint=None,
        hidden_params=None,
        app_id="search",
        headers=None,
        list_view=True,
        grid_view=False,
        pagination_options=(10, 20, 50),
        default_size=10,
        default_page=1,
        facets=None,
        sort=None,
        initial_filters=[],
    )

    def __init__(self, configuration_options):
        """Initialize the search configuration.

        :param endpoint: The URL path to the REST API.
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
        :param default_page: An integer setting the default page.
        """
        options = deepcopy(self.default_options)
        options.update(configuration_options)
        for key, value in options.items():
            setattr(self, key, value)

    @property
    def appId(self):
        """The React appplication id."""
        return self.app_id

    @property
    def initialQueryState(self):
        """Generate initialQueryState."""
        return {
            "hiddenParams": self.hidden_params,
            "layout": "list" if self.list_view else "grid",
            "size": self.default_size,
            "sortBy": self.sort.default,
            "page": self.default_page,
            "filters": self.initial_filters,
        }

    @property
    def searchApi(self):
        """Generate searchAPI configuration."""
        return {
            "axios": {
                "url": self.endpoint,
                "withCredentials": True,
                "headers": self.headers,
            },
            "invenio": {
                "requestSerializer": "InvenioRecordsResourcesRequestSerializer",
            },
        }

    @property
    def layoutOptions(self):
        """Generate the Layout Options.

        :returns: A dict with the options for React-SearchKit JS.
        """
        return {"listView": self.list_view, "gridView": self.grid_view}

    @property
    def sortOptions(self):
        """Format sort options to be used in React-SearchKit JS.

        :returns: A list of dicts with sorting options for React-SearchKit JS.
        """
        return list(self.sort) if self.sort is not None else []

    @property
    def aggs(self):
        """Format the aggs configuration to be used in React-SearchKit JS.

        :returns: A list of dicts for React-SearchKit JS.
        """
        return list(self.facets) if self.facets is not None else []

    @property
    def paginationOptions(self):
        """Format the pagination options to be used in React-SearchKit JS."""
        if (
            not getattr(self, "default_size")
            or self.default_size not in self.pagination_options
        ):
            raise ValueError(
                "Parameter default_size should be part of pagination_options"
            )
        return {
            "resultsPerPage": [
                {"text": str(option), "value": option}
                for option in self.pagination_options
            ],
            "defaultValue": self.default_size,
        }

    @property
    def defaultSortingOnEmptyQueryString(self):
        """Defines the default sorting options when there is no query."""
        return {
            "sortBy": self.sort.default_no_query,
        }

    @classmethod
    def generate(cls, options, **kwargs):
        """Create JSON config for React-Searchkit."""
        generator_object = cls(options)
        config = {
            "appId": generator_object.appId,
            "initialQueryState": generator_object.initialQueryState,
            "searchApi": generator_object.searchApi,
            "sortOptions": generator_object.sortOptions,
            "aggs": generator_object.aggs,
            "layoutOptions": generator_object.layoutOptions,
            "sortOrderDisabled": True,
            "paginationOptions": generator_object.paginationOptions,
            "defaultSortingOnEmptyQueryString": generator_object.defaultSortingOnEmptyQueryString,
        }
        config.update(kwargs)
        return config


#
# Application state context generators, to be used in context processors
#
def sort_config(config_name, sort_options):
    """Sort configuration."""
    return SortConfig(
        sort_options,
        current_app.config[config_name].get("sort", []),
        current_app.config[config_name].get("sort_default", None),
        current_app.config[config_name].get("sort_default_no_query"),
    )


def facets_config(config_name, available_facets):
    """Facets configuration."""
    return FacetsConfig(
        available_facets, current_app.config[config_name].get("facets", [])
    )


def search_app_config(
    config_name,
    available_facets,
    sort_options,
    endpoint,
    headers,
    overrides=None,
    **kwargs
):
    """Search app config.

    Generates search app config expected by React-Searchkit with
    InvenioRecordsResource config.
    """
    opts = dict(
        endpoint=endpoint,
        headers=headers,
        grid_view=False,
        sort=sort_config(config_name, sort_options),
        facets=facets_config(config_name, available_facets),
    )
    opts.update(kwargs)
    overrides = overrides or {}
    return SearchAppConfig.generate(opts, **overrides)
