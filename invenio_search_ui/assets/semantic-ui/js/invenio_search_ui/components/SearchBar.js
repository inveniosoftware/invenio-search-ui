/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import { SearchBar as ReactSearchKitSearchBar, buildUID } from "react-searchkit";
import { createPortal } from "react-dom";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

export const SearchBar = ({ elementId = "header-search-bar", buildUID = buildUID, appName }) => {
  const domElement = document.getElementById(elementId);
  if (domElement) {
    domElement.innerHTML = "";
    return createPortal(<ReactSearchKitSearchBar />, domElement);
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

