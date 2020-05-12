// /*
//  * This file is part of Invenio.
//  * Copyright (C) 2020 CERN.
//  *
//  * Invenio is free software; you can redistribute it and/or modify it
//  * under the terms of the MIT License; see LICENSE file for more details.
//  */

import React, { Component } from "react";
import { Grid, Card, Item, Label } from "semantic-ui-react";
import _truncate from "lodash/truncate";
import _get from "lodash/get";
import {
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  ResultsList,
  ResultsGrid,
  Sort
} from "react-searchkit";
import PropTypes from "prop-types";

export class Results extends Component {
  constructor(props) {
    super(props);

    this.sortValues = this.props.sortValues;
  }

  renderResultsListItem = (result, index) => {
    const metadata = result.metadata;
    return (
      <Item key={index} href={_get(result, "links.html", "#")}>
        <Item.Content>
          <Item.Header>{metadata.title}</Item.Header>
          <Item.Description>
            {_truncate(
              metadata.contributors
                .map(contributor => contributor.name)
                .join("; "),
              { length: 200 }
            )}
          </Item.Description>
          <Item.Extra>
            {metadata.keywords.map(keyword => (
              <Label>{keyword}</Label>
            ))}
          </Item.Extra>
        </Item.Content>
      </Item>
    );
  };

  renderResultsGridItem(result, index) {
    const metadata = result.metadata;
    return (
      <Card fluid key={index} href={_get(result, "links.html", "#")}>
        <Card.Content>
          <Card.Header>{metadata.title}</Card.Header>
          <Card.Description>
            {_truncate(
              metadata.contributors
                .map(contributor => contributor.name)
                .join("; "),
              { length: 200 }
            )}
          </Card.Description>
        </Card.Content>
        <Card.Content extra>
          {metadata.keywords.map(keyword => (
            <Label>{keyword}</Label>
          ))}
        </Card.Content>
      </Card>
    );
  }

  renderCount(totalResults) {
    return (
      <Label size="mini" color="blue">
        {totalResults}
      </Label>
    );
  }

  render() {
    const { total } = this.props.currentResultsState.data;
    const CustomResultsListCmp = () => (
      <ResultsList renderListItem={this.renderResultsListItem} />
    );
    const CustomResultsGridCmp = () => (
      <ResultsGrid renderGridItem={this.renderResultsGridItem} />
    );
    return total ? (
      <Grid relaxed>
        <Grid.Row verticalAlign="middle">
          <Grid.Column width={7}>
            <Count
              renderElement={this.renderCount}
              label={cmp => <>{cmp} result(s) found</>}
            />
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
            <ResultsMultiLayout
              resultsListCmp={CustomResultsListCmp}
              resultsGridCmp={CustomResultsGridCmp}
            />
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
