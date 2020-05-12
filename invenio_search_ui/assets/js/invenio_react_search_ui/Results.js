// /*
//  * This file is part of Invenio.
//  * Copyright (C) 2020 CERN.
//  *
//  * Invenio is free software; you can redistribute it and/or modify it
//  * under the terms of the MIT License; see LICENSE file for more details.
//  */

import React, { Component } from "react";
import { Grid, Card, Image, Item, Label, Divider } from "semantic-ui-react";
import _truncate from "lodash/truncate";
import {
  ActiveFilters,
  Count,
  LayoutSwitcher,
  Pagination,
  ResultsMultiLayout,
  ResultsList,
  ResultsGrid,
  ResultsPerPage,
  Sort
} from "react-searchkit";

const SpanWithMargin = ({ text, margin }) => {
  const size = "0.5em";
  let style;
  switch (margin) {
    case "left":
      style = { marginLeft: size };
      break;
    case "right":
      style = { marginRight: size };
      break;
    default:
      style = { margin: `0 ${size}` };
  }
  return <span style={style}>{text}</span>;
};

export class Results extends Component {
  constructor(props) {
    super(props);

    this.sortValues = this.props.sortValues;
    this.resultsPerPageValues = this.props.resultsPerPageValues;
  }

  renderResultsListItem = (result, index) => {
    const metadata = result.metadata;
    return (
      <Item key={index} href={`#`}>
        <Item.Image
          size="small"
          src={result.imageSrc || "https://placehold.it/200"}
        />
        <Item.Content>
          <Item.Header>{metadata.title}</Item.Header>
          <Item.Description>
            {_truncate(metadata.keywords.join(","), { length: 200 })}
          </Item.Description>
        </Item.Content>
      </Item>
    );
  };

  renderResultsGridItem(result, index) {
    const metadata = result.metadata;
    return (
      <Card fluid key={index} href={`#`}>
        <Image src={result.imageSrc || "https://placehold.it/200"} />
        <Card.Content>
          <Card.Header>{metadata.title}</Card.Header>
          <Card.Description>
            {_truncate(metadata.keywords.join(","), { length: 200 })}
          </Card.Description>
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
      <>
        <Grid relaxed>
          <Grid.Row verticalAlign="middle">
            <Grid.Column width={7}>
              <Count renderElement={this.renderCount} label={(cmp)=> <>{cmp} result(s) found</>}/>
              <br />
            </Grid.Column>
            <Grid.Column width={7} textAlign="right">
              <SpanWithMargin text="Sort by" />
              <Sort values={this.sortValues} />
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
      </>
    ) : null;
  }
}

Results.propTypes = {};

Results.defaultProps = {};
