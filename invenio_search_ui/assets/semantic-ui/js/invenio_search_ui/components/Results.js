/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
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

export const Results = ({ currentResultsState = {} }) => {
  const { total } = currentResultsState.data;
  const { sortOptions, layoutOptions, paginationOptions } = useContext(
    SearchConfigurationContext
  );
  let multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  return (
    (total || null) && (
      <Overridable id={"SearchApp.results"} {...{currentResultsState, sortOptions, layoutOptions, paginationOptions}}>
        <Grid relaxed>
          <Grid.Row verticalAlign="middle">
            <Grid.Column width={multipleLayouts ? 5 : 8}>
              <Count label={(cmp) => <>{cmp} result(s) found</>} />
              <br />
            </Grid.Column>
            <Grid.Column width={4} textAlign="right">
              <ResultsPerPage
                values={paginationOptions.resultsPerPage}
                label={(cmp) => <> {cmp} results per page</>}
                defaultValue={paginationOptions.defaultValue}
              />
            </Grid.Column>
            <Grid.Column width={4} textAlign="right">
              {sortOptions && (
                <Sort values={sortOptions} label={(cmp) => <>sort by {cmp}</>} />
              )}
            </Grid.Column>
            {multipleLayouts ? (
              <Grid.Column width={3} textAlign="right">
                <LayoutSwitcher defaultLayout="list" />
              </Grid.Column>
            ) : null}
          </Grid.Row>
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
          <Grid.Row verticalAlign="middle" textAlign="center">
            <Grid.Column>
              <Pagination />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Overridable>
    )
  );
};
