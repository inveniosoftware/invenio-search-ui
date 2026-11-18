/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import { Component } from "react";
import { Dropdown, Icon } from "semantic-ui-react";
import PropTypes from "prop-types";

export class DropdownSort extends Component {
  render() {
    const {
      options,
      currentSortBy,
      currentSortOrder,
      onValueChange,
      ariaLabel,
      selectOnNavigation,
    } = this.props;

    const sortBy = Array.isArray(currentSortBy) ? currentSortBy[0] : currentSortBy;
    const selectedOption = options.find(
      (option) =>
        option.sortBy === sortBy &&
        (!option.sortOrder || !currentSortOrder || option.sortOrder === currentSortOrder)
    );
    const selectedValue = selectedOption?.value;
    const parsedOptions = options.map(({ value, text }) => {
      const selected = value === selectedValue;
      return { key: value, text, value, disabled: selected, selected };
    });

    return (
      <Dropdown
        icon="sort"
        button
        labeled
        item
        trigger={
          <span className="flex align-items-center">
            {selectedOption?.text ?? ariaLabel}
            <Icon name="dropdown" />
          </span>
        }
        options={parsedOptions}
        value={selectedValue ?? ""}
        onChange={(_, { value }) => onValueChange(value)}
        aria-label={ariaLabel}
        selectOnNavigation={selectOnNavigation}
        selectOnBlur={false}
        size="large"
        className="icon fluid-mobile"
      />
    );
  }
}

DropdownSort.propTypes = {
  options: PropTypes.array.isRequired,
  currentSortBy: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.arrayOf(PropTypes.string),
  ]),
  currentSortOrder: PropTypes.string,
  overridableId: PropTypes.string,
  ariaLabel: PropTypes.string,
  selectOnNavigation: PropTypes.bool,
  onValueChange: PropTypes.func.isRequired,
};

export class DropdownFilter extends Component {
  onChangeFilter = (e, data) => {
    const { updateQueryState, currentQueryState } = this.props;
    currentQueryState.filters.push(JSON.parse(data.value));
    updateQueryState(currentQueryState);
  };

  render() {
    const {
      filterKey,
      filterValues,
      filterLabel = "",
      currentQueryState,
      updateQueryState,
      loading,
      ...uiProps
    } = this.props;
    const options = filterValues.map((filterValue) => {
      const value = [filterKey, filterValue.key];
      const disabled = currentQueryState.filters.some(
        (filter) => JSON.stringify(value) === JSON.stringify(filter)
      );
      return {
        key: filterValue.key,
        text: filterValue.label,
        value: JSON.stringify(value),
        disabled: disabled,
      };
    });

    return (
      <Dropdown
        icon="filter"
        labeled
        item
        button
        trigger={
          <span className="flex align-items-center">
            {filterLabel}
            <Icon name="dropdown" />
          </span>
        }
        options={options}
        onChange={this.onChangeFilter}
        selectOnBlur={false}
        value={null}
        loading={loading}
        className="icon fluid-mobile"
        {...uiProps}
      />
    );
  }
}

DropdownFilter.propTypes = {
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  filterKey: PropTypes.string.isRequired,
  filterValues: PropTypes.array.isRequired,
  filterLabel: PropTypes.string.isRequired,
};
