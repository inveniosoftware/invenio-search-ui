/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React from "react";
import Overridable, {
  OverridableContext,
  overrideStore,
} from "react-overridable";
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
import { Results, ResultOptions } from "./Results";
import { SearchBar } from "./SearchBar";
import { SearchConfigurationContext } from "./context";

const OnResults = withState(Results);
const ResultOptionsWithState = withState(ResultOptions);

export const SearchAppFacets = ({ aggs }) => {
  return (
    <Overridable id={"SearchApp.facets"} aggs={aggs}>
      <>
        {aggs.map((agg) => (
          <BucketAggregation key={agg.title} title={agg.title} agg={agg} />
        ))}
      </>
    </Overridable>
  );
};

export const SearchAppResultsPane = ({ layoutOptions }) => {
  return (
    <Overridable
      id={"SearchApp.resultsPane"}
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

export const SearchApp = ({ config, appName }) => {
  const searchApi = new InvenioSearchApi(config.searchApi);
  return (
    <OverridableContext.Provider value={overrideStore.getAll()}>
      <SearchConfigurationContext.Provider value={config}>
        <ReactSearchKit
          searchApi={searchApi}
          appName={appName}
          initialQueryState={config.initialQueryState}
        >
          <Overridable id={"SearchApp.layout"}>
            <Container>
              <Overridable id={"SearchApp.searchbarContainer"}>
                <Grid relaxed padded>
                  <Grid.Row>
                    <Grid.Column width={4} />
                    <Grid.Column width={12}>
                      <Overridable id={"SearchApp.searchbar"}>
                        <SearchBar />
                      </Overridable>
                    </Grid.Column>
                  </Grid.Row>
                </Grid>
              </Overridable>
              <Grid relaxed>
                <Grid.Row
                  textAlign='right'
                  columns={2}
                  className="result-options"
                >
                  <Grid.Column width={4}/>
                  <Grid.Column width={12}>
                    <ResultOptionsWithState
                      sortOptions={config.sortOptions}
                      layoutOptions={config.layoutOptions}
                    />
                  </Grid.Column>
                </Grid.Row>
                <Grid.Row columns={2}>
                  <Grid.Column width={4}>
                    <SearchAppFacets aggs={config.aggs} />
                  </Grid.Column>
                  <Grid.Column width={12}>
                    <SearchAppResultsPane
                      layoutOptions={config.layoutOptions}
                    />
                  </Grid.Column>
                </Grid.Row>
              </Grid>
            </Container>
          </Overridable>
        </ReactSearchKit>
      </SearchConfigurationContext.Provider>
    </OverridableContext.Provider>
  );
};

SearchApp.propTypes = {
  config: PropTypes.shape({
    searchApi: PropTypes.object.isRequired, // same as ReactSearchKit.searchApi
    initialQueryState: PropTypes.object,
    aggs: PropTypes.arrayOf(
      PropTypes.shape({
        title: PropTypes.string,
        aggName: PropTypes.string,
        access_right: PropTypes.string,
        mapping: PropTypes.object,
      })
    ),
    sortOptions: PropTypes.arrayOf(
      PropTypes.shape({
        default: PropTypes.bool,
        defaultOnEmptyString: PropTypes.bool,
        sortBy: PropTypes.string,
        sortOrder: PropTypes.string,
        text: PropTypes.string,
      })
    ),
    paginationOptions: PropTypes.shape({
      defaultValue: PropTypes.number,
      resultsPerPage: PropTypes.arrayOf(
        PropTypes.shape({
          text: PropTypes.string,
          value: PropTypes.number,
        })
      ),
    }),
    layoutOptions: PropTypes.shape({
      listView: PropTypes.bool.isRequired,
      gridView: PropTypes.bool.isRequired,
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
      listView: true,
      gridView: false,
    },
  },
  appName: null,
};
