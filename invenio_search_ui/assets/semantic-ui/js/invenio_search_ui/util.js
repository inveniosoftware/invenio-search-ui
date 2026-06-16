/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import { createRoot } from "react-dom/client";
import { loadComponents } from "@js/invenio_theme/templates";
import _camelCase from "lodash/camelCase";
import { Fragment } from "react";
import { SearchApp } from "./components";

/**
 * Initialize React search application.
 * @function
 * @param {object} defaultComponents - default components to load if no overriden have been registered.
 * @param {boolean} autoInit - if true then the application is getting registered to the DOM.
 * @param {string} autoInitDataAttr - data attribute to register application to DOM and retrieve config.
 * @param {object} multi - enable multiple search application support.
 *    If true, the application is namespaced using `config.appId`. That allows
 *    users to override each application's components using `appId` as a prefix.
 * @returns {object} frontend compatible record object
 */
export function createSearchAppInit(
  defaultComponents,
  autoInit = true,
  autoInitDataAttr = "invenio-search-config",
  multi = false,
  ContainerComponent = Fragment,
) {

  const initSearchApp = (rootElement) => {
    if (rootElement.dataset.reactRootMounted) return;
    rootElement.dataset.reactRootMounted = "true";
    const { appId, ...config } = JSON.parse(
      rootElement.dataset[_camelCase(autoInitDataAttr)]
    );
    loadComponents(appId, defaultComponents).then((res) => {
      const root = createRoot(rootElement);

      root.render(<ContainerComponent>
        <SearchApp
          config={config}
          // Use appName to namespace application components when overriding
          {...(multi && { appName: appId })}
        />
      </ContainerComponent>);
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
