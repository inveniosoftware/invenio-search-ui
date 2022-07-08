/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { Component } from "react";
import { withState } from "react-searchkit";
import { Search, Label } from "semantic-ui-react";
import { i18next } from "@translations/invenio_search_ui/i18next";
import PropTypes from "prop-types";

const resultRenderer = ({ text }, queryString) => {
  return (
    <div className="flex">
      <div className="truncated pt-5">{queryString}</div>
      <Label className="right-floated">{text}</Label>
    </div>
  );
};

export class MultipleOptionsSearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      queryString: "",
    };
  }

  render() {
    const { placeholder, options } = this.props;
    const { queryString } = this.state;

    return (
      <Search
        fluid
        onResultSelect={(e, { result }) => {
          const { value: url } = result;
          window.location = `${url}?q=${queryString}`;
        }}
        onSearchChange={(e, { value }) => {
          this.setState({ queryString: value });
        }}
        resultRenderer={(props) => resultRenderer(props, queryString)}
        results={options}
        value={queryString}
        placeholder={placeholder}
        selectFirstResult
      />
    );
  }
}

MultipleOptionsSearchBar.propTypes = {
  options: PropTypes.array.isRequired,
  placeholder: PropTypes.string,
};

MultipleOptionsSearchBar.defaultProps = {
  placeholder: i18next.t("Search"),
};

export class MultipleOptionsSearchBarCmp extends Component {
  onBtnSearchClick = () => {
    const { queryString, updateQueryState, currentQueryState } = this.props;
    updateQueryState({ ...currentQueryState, queryString });
  };

  render() {
    const { placeholder, queryString, onInputChange, options } = this.props;

    return (
      <Search
        fluid
        onResultSelect={(e, { result }) => {
          const { value: url } = result;
          if (window.location.pathname === url) {
            this.onBtnSearchClick();
          } else {
            window.location = `${url}?q=${queryString}`;
          }
        }}
        onSearchChange={(e, { value }) => {
          onInputChange(value);
        }}
        resultRenderer={(props) => resultRenderer(props, queryString)}
        results={options}
        value={queryString}
        placeholder={placeholder}
        selectFirstResult
      />
    );
  }
}

MultipleOptionsSearchBarCmp.propTypes = {
  options: PropTypes.array.isRequired,
  queryString: PropTypes.string.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  onInputChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string,
};

MultipleOptionsSearchBarCmp.defaultProps = {
  placeholder: i18next.t("Search"),
};

export const MultipleOptionsSearchBarRSK = withState(MultipleOptionsSearchBarCmp);
