import React from "react";
import { Card, Item, Label } from "semantic-ui-react";
import _truncate from "lodash/truncate";
import _get from "lodash/get";
import { overrideStore } from "react-overridable";


const SearchUIResultsListItem = ({result, index}) => {
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

const SearchUIResultsGridItem = ({result, index}) =>{
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

overrideStore.add("ResultsList.item", SearchUIResultsListItem)
overrideStore.add("ResultsGrid.item", SearchUIResultsGridItem)
