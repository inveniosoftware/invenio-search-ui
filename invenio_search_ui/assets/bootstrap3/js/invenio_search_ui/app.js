/*
 * SPDX-FileCopyrightText: 2015-2018 CERN.
 * SPDX-License-Identifier: MIT
 */

import "d3";
import angular from "angular";
import "angular-loading-bar";
import "invenio-search-js/dist/invenio-search-js";

// When the DOM is ready bootstrap the `invenio-serach-js`
angular.element(document).ready(function() {
  angular.bootstrap(document.getElementById("invenio-search"), [
    "angular-loading-bar",
    "invenioSearch"
  ]);
});
