/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import React from "react";
import {
  SearchBar as ReactSearchKitSearchBar,
  buildUID,
} from "react-searchkit";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

export const SearchBar = ({ elementId, buildUID, appName }) => {
  const domElement = document.getElementById(elementId);
  if (domElement) {
    domElement.innerHTML = "";
    return ReactDOM.createPortal(<ReactSearchKitSearchBar />, domElement);
  }
  return (
    <Overridable id={buildUID("SearchApp.searchbar", "", appName)}>
      <ReactSearchKitSearchBar />
    </Overridable>
  );
};

SearchBar.propTypes = {
  elementId: PropTypes.string,
};

SearchBar.defaultProps = {
  elementId: "header-search-bar",
  buildUID: buildUID,
};
