// /*
//  * This file is part of Invenio.
//  * Copyright (C) 2020 CERN.
//  *
//  * Invenio is free software; you can redistribute it and/or modify it
//  * under the terms of the MIT License; see LICENSE file for more details.
//  */

import React, { Component } from "react";
import { Grid} from "semantic-ui-react";
import {
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  Sort
} from "react-searchkit";
import PropTypes from "prop-types";

export class Results extends Component {
  constructor(props) {
    super(props);

    this.sortValues = this.props.sortValues;
  }

  render() {
    const { total } = this.props.currentResultsState.data;
    return total ? (
      <Grid relaxed>
        <Grid.Row verticalAlign="middle">
          <Grid.Column width={7}>
            <Count label={cmp => <>{cmp} result(s) found</>} />
            <br />
          </Grid.Column>
          <Grid.Column width={7} textAlign="right">
            <Sort values={this.sortValues} label={cmp => <>sort by {cmp}</>} />
          </Grid.Column>
          <Grid.Column width={2} textAlign="right">
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
  sortValues: PropTypes.array.isRequired
};

Results.defaultProps = {};
