/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React from "react";
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
import { SearchBar } from "./SearchBar";

const OnResults = withState(Results);
export const SearchConfigurationContext = React.createContext({});

export const SearchApp = ({ config, appName }) => {
  const searchApi = new InvenioSearchApi(config.searchApi);

  return (
    <OverridableContext.Provider value={overrideStore.getAll()}>
      <SearchConfigurationContext.Provider value={config}>
        <ReactSearchKit searchApi={searchApi} appName={appName} initialQueryState={config.initialQueryState}>
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
                    <OnResults sortValues={config.sortOptions} layoutOptions={config.layoutOptions} />
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
    searchApi: PropTypes.object.isRequired, //same as ReactSearchKit.searchApi
    initialQueryState: PropTypes.object,
    aggs: PropTypes.arrayOf(PropTypes.shape({
      title: PropTypes.string,
      aggName: PropTypes.string,
      access_right: PropTypes.string,
      mapping: PropTypes.object
    })),
    sortOptions: PropTypes.arrayOf(PropTypes.shape({
      default: PropTypes.bool,
      defaultOnEmptyString: PropTypes.bool,
      sortBy: PropTypes.string,
      sortOrder: PropTypes.string,
      text: PropTypes.string
    })),
    paginationOptions: PropTypes.shape({
      defaultValue: PropTypes.number,
      resultsPerPage: PropTypes.arrayOf(PropTypes.shape({
        text: PropTypes.string,
        value: PropTypes.number
      }))
    }),
    layoutOptions: PropTypes.shape({
      listView: PropTypes.bool.isRequired,
      gridView: PropTypes.bool.isRequired
    }).isRequired,
  }).isRequired,
  appName: PropTypes.string,
};

SearchApp.defaultProps = {
  config: {
  searchApi: {
    url: "",
    withCredentials: false,
    headers: {},
  },
  initialQueryState: {},
  aggs: [],
  sortOptions: [],
  paginationOptions: {},
  layoutOptions: {
    'listView': true,
    'gridView': false
  }
},
  appName: null,
};
