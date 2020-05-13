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
import PropTypes from "prop-types";
import { Results } from "./Results";
import { InvenioSearchApi } from "react-searchkit";
import { OverridableContext, overrideStore } from "react-overridable";

const OnResults = withState(Results);

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
      headers: { Accept: this.props.config.mimetype }
    });

    return (
      <OverridableContext.Provider value={overrideStore.getAll()}>
        <ReactSearchKit searchApi={config} appName={this.props.appName}>
          <Container>
            <Grid>
              <Grid.Row>
                <Grid.Column width={4} />
                <Grid.Column width={12}>
                  <SearchBar />
                </Grid.Column>
              </Grid.Row>
            </Grid>
            <Grid relaxed padded>
              <Grid.Row columns={2}>
                <Grid.Column width={4}>
                  {this.props.config.aggs.map(agg => (
                    <BucketAggregation
                      key={agg.title}
                      title={agg.title}
                      agg={{
                        field: agg.field,
                        aggName: agg.aggName
                      }}
                    />
                  ))}
                </Grid.Column>
                <Grid.Column width={12}>
                  <ResultsLoader>
                    <EmptyResults />
                    <Error />
                    <OnResults sortValues={this.props.config.sort_options} />
                  </ResultsLoader>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Container>
        </ReactSearchKit>
      </OverridableContext.Provider>
    );
  }
}

App.propTypes = {
  config: PropTypes.object.isRequired,
  appName: PropTypes.string,
}
