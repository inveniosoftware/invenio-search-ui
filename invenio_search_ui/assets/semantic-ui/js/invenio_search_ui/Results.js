/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React, { Component } from "react";
import {
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  Sort,
} from "react-searchkit";
import { Grid } from "semantic-ui-react";

export class Results extends Component {
  render() {
    const { sortValues, currentResultsState } = this.props;
    const { total } = currentResultsState.data;
    return total ? (
      <Grid relaxed>
        <Grid.Row verticalAlign="middle">
          <Grid.Column width={7}>
            <Count label={(cmp) => <>{cmp} result(s) found</>} />
            <br />
          </Grid.Column>
          <Grid.Column width={6} textAlign="right">
            {sortValues && (
              <Sort values={sortValues} label={(cmp) => <>sort by {cmp}</>} />
            )}
          </Grid.Column>
          <Grid.Column width={3} textAlign="right">
            <LayoutSwitcher defaultLayout="list" />
          </Grid.Column>
        </Grid.Row>
        <Grid.Row>
          <Grid.Column>
            <ResultsMultiLayout />
          </Grid.Column>
        </Grid.Row>
        <Grid.Row verticalAlign="middle" textAlign="center">
          <Grid.Column>
            <Pagination />
          </Grid.Column>
        </Grid.Row>
      </Grid>
    ) : null;
  }
}

Results.propTypes = {
  sortValues: PropTypes.array,
};

Results.defaultProps = {
  sortValues: [],
};
