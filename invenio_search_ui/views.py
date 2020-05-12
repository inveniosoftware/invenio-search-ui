# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI for Invenio-Search."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, json, render_template

blueprint = Blueprint(
    'invenio_search_ui',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/search')
def search():
    """Search page ui."""
    return render_template(current_app.config['SEARCH_UI_SEARCH_TEMPLATE'])


def sorted_options(sort_options):
    """Sort sort options for display.

    :param sort_options: A dictionary containing the field name as key and
        asc/desc as value.
    :returns: A dictionary with sorting options for Invenio-Search-JS.
    """
    return [
        {
            'title': v['title'],
            'value': ('-{0}'.format(k)
                      if v.get('default_order', 'asc') == 'desc' else k),
        }
        for k, v in
        sorted(sort_options.items(), key=lambda x: x[1].get('order', 0))
    ]


def searchkit_sort_options(sort_options, default_sort):
    """Sort and map sort options for display.

        :param sort_options: A dictionary containing the field name as key and
            asc/desc as value.
        :returns: A dictionary with sorting options for Invenio-Search-JS
        with react-searchkit.
        """
    return [
        {
            'text': v['title'],
            'sortBy': k,
            'sortOrder': v.get('default_order', 'asc'),
            'default': default_sort["query"] == k,
            'defaultOnEmptyString': default_sort["noquery"] == k,
        }
        for k, v in
        sorted(sort_options.items(), key=lambda x: x[1].get('order', 0))
    ]


def searchkit_aggs(aggs):
    """Format the aggregation configuration to be used in Invenio-Search-JS.

    :param aggs: A dictionary with aggregation configuration
    :returns: A formated dictionary.
    """
    return [
        {
            'title': k.capitalize(),
            'aggName': k,
            'field': v['terms']['field'],
        }
        for k, v in aggs.items()
    ]


@blueprint.app_template_filter('format_sortoptions')
def format_sortoptions(sort_options):
    """Create sort options JSON dump for Invenio-Search-JS."""
    return json.dumps({
        'options': sorted_options(sort_options)
    })


@blueprint.app_template_filter('format_config')
def format_config(config, endpoint_name):
    """Create config JSON dump for Invenio-Search-JS."""

    config_sort_options = config.get('RECORDS_REST_SORT_OPTIONS', {}).get(
        endpoint_name)
    config_default_sort = config.get('RECORDS_REST_DEFAULT_SORT', {}).get(
        endpoint_name)

    return json.dumps({
        'api': config.get('SEARCH_UI_SEARCH_API'),
        'mimetype': config.get('SEARCH_UI_SEARCH_MIMETYPE',
                               'application/json'),
        "sort_options": searchkit_sort_options(
            config_sort_options, config_default_sort
        ),
        "aggs": searchkit_aggs(config.get('RECORDS_REST_FACETS', {}).get(
            endpoint_name).get("aggs", {}))
    })
