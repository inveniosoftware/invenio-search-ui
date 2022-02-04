/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 * Copyright (C) 2021 Graz University of Technology.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import Overridable from "react-overridable";
import React, { useContext } from "react";
import {
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  Sort,
  ResultsList,
  ResultsGrid,
  ResultsPerPage,
} from "react-searchkit";
import { Grid } from "semantic-ui-react";
import { SearchConfigurationContext } from "./context";
import { i18next } from "@translations/invenio_app_rdm/i18next";

export const Results = ({ currentResultsState = {} }) => {
  const { total } = currentResultsState.data;
  const { sortOptions, layoutOptions, paginationOptions, buildUID } =
    useContext(SearchConfigurationContext);
  const multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  return (
    (total || null) && (
      <Overridable
        id={buildUID("SearchApp.results")}
        {...{
          sortOptions,
          paginationOptions,
          currentResultsState,
          layoutOptions,
        }}
      >
        <Grid relaxed>
          <Grid.Row>
            <Grid.Column>
              {multipleLayouts ? (
                <ResultsMultiLayout />
              ) : layoutOptions.listView ? (
                <ResultsList />
              ) : (
                <ResultsGrid />
              )}
            </Grid.Column>
          </Grid.Row>
          <Grid.Row verticalAlign="middle">
            <Grid.Column width={4}></Grid.Column>
            <Grid.Column width={8} textAlign="center">
              <Pagination
                options={{
                  size: "mini",
                  showFirst: false,
                  showLast: false,
                }}
              />
            </Grid.Column>
            <Grid.Column textAlign="right" width={4}>
              <ResultsPerPage
                values={paginationOptions.resultsPerPage}
                label={(cmp) => <> {cmp} results per page</>}
              />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Overridable>
    )
  );
};

export const ResultOptions = ({ currentResultsState = {} }) => {
  const { total } = currentResultsState.data;
  const {
    sortOptions,
    paginationOptions,
    sortOrderDisabled,
    layoutOptions,
    buildUID,
  } = useContext(SearchConfigurationContext);
  const multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  return (
    (total || null) && (
      <Overridable
        id={buildUID("SearchApp.resultOptions")}
        {...{
          currentResultsState,
          sortOptions,
          paginationOptions,
          layoutOptions,
        }}
      >
        <Grid>
          <Grid.Row verticalAlign="middle">
            <Grid.Column textAlign="left" width={multipleLayouts ? 5 : 8}>
              <Count label={(cmp) => <>{cmp} result(s) found</>} />
              <br />
            </Grid.Column>
            <Grid.Column width={8} textAlign="right">
              {sortOptions && (
                <Overridable
                  id={buildUID("SearchApp.sort")}
                  options={sortOptions}
                >
                  <Sort
                    sortOrderDisabled={sortOrderDisabled || false}
                    values={sortOptions}
                    ariaLabel={i18next.t("Sort")}
                  />
                </Overridable>
              )}
            </Grid.Column>
            {multipleLayouts ? (
              <Grid.Column width={3} textAlign="right">
                <LayoutSwitcher />
              </Grid.Column>
            ) : null}
          </Grid.Row>
        </Grid>
      </Overridable>
    )
  );
};
