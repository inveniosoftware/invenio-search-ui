/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React, { Component, useContext } from "react";
import {
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  Sort,
  ResultsList,
  ResultsGrid
} from "react-searchkit";
import { Grid } from "semantic-ui-react";
import { SearchConfigurationContext } from "./SearchApp";

export const Results = ({
  sortValues = [],
  currentResultsState = {}
}) => {
  const { total } = currentResultsState.data;
  const { layoutOptions } = useContext(SearchConfigurationContext);
  let layoutOptions = layoutOptions;
  let multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  if (total) {
    return (
      <Grid relaxed>
        <Grid.Row verticalAlign="middle">
          <Grid.Column width={multipleLayouts ? 7 : 10}>
            <Count label={(cmp) => <>{cmp} result(s) found</>} />
            <br />
          </Grid.Column>
          <Grid.Column width={6} textAlign="right">
            {sortValues && (
              <Sort values={sortValues} label={(cmp) => <>sort by {cmp}</>} />
            )}
          </Grid.Column>
          {multipleLayouts ?
            <Grid.Column width={3} textAlign="right">
              <LayoutSwitcher defaultLayout="list" />
            </Grid.Column>
            : null}
        </Grid.Row>
        <Grid.Row>
          <Grid.Column>
            {multipleLayouts ?
              <ResultsMultiLayout />
              : layoutOptions.listView ?
                <ResultsList /> :
                <ResultsGrid />
            }
          </Grid.Column>
        </Grid.Row>
        <Grid.Row verticalAlign="middle" textAlign="center">
          <Grid.Column>
            <Pagination />
          </Grid.Column>
        </Grid.Row>
      </Grid>
    )
  }
  else {
    return null;
  }
}

