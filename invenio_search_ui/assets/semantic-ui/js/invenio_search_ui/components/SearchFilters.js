/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import { DropdownFilter } from "@js/invenio_search_ui/components";
import PropTypes from "prop-types";
import { Component } from "react";
import { withState } from "react-searchkit";

export class SearchFiltersComponent extends Component {
  render() {
    const {
      currentQueryState,
      updateQueryState,
      currentResultsState,
      customFilters = undefined,
    } = this.props;
    const filters = customFilters
      ? customFilters
      : currentResultsState.data.aggregations;
    return (
      <>
        {Object.entries(filters).map((filter) => (
          <DropdownFilter
            key={filter[0]}
            filterKey={filter[0]}
            filterLabel={filter[1].label}
            aria-label={filter[1].label}
            filterValues={filter[1].buckets}
            currentQueryState={currentQueryState}
            updateQueryState={updateQueryState}
            loading={currentResultsState.loading}
            size="large"
          />
        ))}
      </>
    );
  }
}

SearchFiltersComponent.propTypes = {
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  customFilters: PropTypes.object,
};

export const SearchFilters = withState(SearchFiltersComponent);
