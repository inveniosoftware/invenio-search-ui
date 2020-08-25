/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import ReactDOM from "react-dom";
import { SearchApp } from "./components";
import { loadComponents } from "@js/invenio_theme/templates";
import _camelCase from "lodash/camelCase";

export function createSearchAppInit(
  defaultComponents,
  autoInit = true,
  autoInitDataAttr = "invenio-search-config"
) {
  const initSearchApp = (rootElement) => {
    const config = JSON.parse(
      rootElement.dataset[_camelCase(autoInitDataAttr)]
    );
    loadComponents(config.appId, defaultComponents).then((res) => {
      ReactDOM.render(<SearchApp config={config} />, rootElement);
    });
  };

  if (autoInit) {
    const searchAppElements = document.querySelectorAll(
      `[data-${autoInitDataAttr}]`
    );
    for (const appRootElement of searchAppElements) {
      initSearchApp(appRootElement);
    }
  } else {
    return initSearchApp;
  }
}
