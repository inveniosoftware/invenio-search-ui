/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { Component } from "react";
import { Container, Grid } from "semantic-ui-react";
import {
  ReactSearchKit,
  SearchBar,
  BucketAggregation,
  EmptyResults,
  Error,
  ResultsLoader,
  withState
} from "react-searchkit";
import { Results } from "./Results";
import { InvenioSearchApi } from "react-searchkit";

import "semantic-ui-css/semantic.min.css";

const OnResults = withState(Results);

const sortValues = [
  {
    text: "Most viewed",
    sortBy: "mostviewed",
    sortOrder: "asc",
    defaultOnEmptyString: true
  },
  {
    text: "Least viewed",
    sortBy: "mostviewed",
    sortOrder: "desc"
  },
  {
    text: "Newest",
    sortBy: "mostrecent",
    sortOrder: "asc",
    default: true
  },
  {
    text: "Oldest",
    sortBy: "mostrecent",
    sortOrder: "desc"
  }
];

const resultsPerPageValues = [
  {
    text: "10",
    value: 10
  },
  {
    text: "20",
    value: 20
  },
  {
    text: "50",
    value: 50
  }
];

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = { activeIndex: -1 };
  }

  render() {

    const config = new InvenioSearchApi({
      axios: {
        url: this.props.config.api,
        withCredentials: true
      },
      timeout: 5000,
      headers: { Accept: this.props.config.mimetype, }
    });

    return (
      <ReactSearchKit searchApi={config}>
        <Container>
          <Grid>
            <Grid.Row>
              <Grid.Column width={3} />
              <Grid.Column width={10}>
                <SearchBar />
              </Grid.Column>
              <Grid.Column width={3} />
            </Grid.Row>
          </Grid>
          <Grid relaxed style={{ padding: "2em 0" }}>
            <Grid.Row columns={2}>
              <Grid.Column width={4}>
                <BucketAggregation
                  title="File types"
                  agg={{
                    field: "file_type",
                    aggName: "file_type"
                  }}
                />
                <br />
                <BucketAggregation
                  title="Keywords"
                  agg={{
                    field: "keywords",
                    aggName: "keywords"
                  }}
                />
                <br />
                <BucketAggregation
                  title="Types"
                  agg={{
                    field: "resource_type.type",
                    aggName: "type",
                    childAgg: {
                      field: "resource_type.subtype",
                      aggName: "subtype"
                    }
                  }}
                />
                <br />
              </Grid.Column>
              <Grid.Column width={12}>
                <ResultsLoader>
                  <EmptyResults />
                  <Error />
                  <OnResults
                    sortValues={sortValues}
                    resultsPerPageValues={resultsPerPageValues}
                  />
                </ResultsLoader>
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Container>
      </ReactSearchKit>
    );
  }
}
