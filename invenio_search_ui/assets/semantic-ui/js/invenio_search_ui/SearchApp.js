/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React, { Component, useContext } from "react";
import { OverridableContext, overrideStore } from "react-overridable";
import {
  BucketAggregation,
  EmptyResults,
  Error,
  InvenioSearchApi,
  ReactSearchKit,
  ResultsLoader,
  withState,
} from "react-searchkit";
import { Container, Grid } from "semantic-ui-react";
import { Results } from "./Results";
import SearchBar from "./SearchBar";

const OnResults = withState(Results);
export const SearchConfigurationContext = React.createContext({});

export const SearchApp = ({ config, appName }) => {
  const searchApi = new InvenioSearchApi(config.searchApi);

  return (
    <OverridableContext.Provider value={overrideStore.getAll()}>
      <SearchConfigurationContext.Provider value={config}>
        <ReactSearchKit searchApi={searchApi} appName={appName}>
          <Container>
            <Grid relaxed padded>
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
                  {config.aggs.map((agg) => (
                    <BucketAggregation
                      key={agg.title}
                      title={agg.title}
                      agg={{
                        field: agg.field,
                        aggName: agg.aggName,
                      }}
                    />
                  ))}
                </Grid.Column>
                <Grid.Column width={12}>
                  <ResultsLoader>
                    <EmptyResults />
                    <Error />
                    <OnResults sortValues={config.sort_options} layoutOptions={config.layoutOptions} />
                  </ResultsLoader>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Container>
        </ReactSearchKit>
      </SearchConfigurationContext.Provider>
    </OverridableContext.Provider>
  )
}

SearchApp.propTypes = {
  config: PropTypes.shape({
    api: PropTypes.string,
    mimetype: PropTypes.string,
    aggs: PropTypes.arrayOf(PropTypes.shape({
      title: PropTypes.string,
      aggName: PropTypes.string,
    })),
    sort_options: PropTypes.array.isRequired,
  }).isRequired,
  appName: PropTypes.string,
};

SearchApp.defaultProps = {
  config: {
    api: "",
    mimetype: "",
    aggs: [],
    sort_options: [],
  },
  appName: null,
};
