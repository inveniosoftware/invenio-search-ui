/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */
import { Results } from "./Results";
import React from "react";
import {
  EmptyResults,
  Error,
  ResultsLoader,
  withState,
  buildUID,
} from "react-searchkit";
import Overridable from "react-overridable";

const OnResults = withState(Results);

export const SearchAppResultsPane = ({ layoutOptions, appName }) => {
  const buildOverridableUID = (element) => buildUID(element, "", appName);
  return (
    <Overridable
      id={buildOverridableUID("SearchApp.resultsPane", "", appName)}
      layoutOptions={layoutOptions}
    >
      <ResultsLoader>
        <EmptyResults />
        <Error />
        <OnResults />
      </ResultsLoader>
    </Overridable>
  );
};
