/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { Component } from "react";
import { SearchBar } from "react-searchkit";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";


export default class InvenioSearchUISearchBar extends Component {

  render() {
    if (!this.props.searchBarUID){
      return <SearchBar/>
    }
    const searchNode = document.getElementById(this.props.searchBarUID);
    if (searchNode) {
      searchNode.innerHTML = "";
      return ReactDOM.createPortal(<SearchBar />, searchNode);
    }
    return <SearchBar/>;
  }
}

InvenioSearchUISearchBar.propTypes = {
  searchBarUID: PropTypes.string,
}
