/*
 * This file is part of Invenio.
 * Copyright (C) 2015-2018 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
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
