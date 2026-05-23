/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import _get from "lodash/get";
import _truncate from "lodash/truncate";
import React from "react";
import { Item, Label } from "semantic-ui-react";

export const ResultsListItem = ({ result }) => {
  const metadata = result.metadata;
  return (
    <Item href={_get(result, "links.html", "#")}>
      <Item.Content>
        <Item.Header>{metadata.title}</Item.Header>
        <Item.Description>
          {_truncate(
            metadata.contributors
              .map((contributor) => contributor.name)
              .join("; "),
            { length: 200 }
          )}
        </Item.Description>
        <Item.Extra>
          {metadata.keywords &&
            metadata.keywords.map((keyword, idx) => (
              <Label key={idx}>{keyword}</Label>
            ))}
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};
