/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import _get from "lodash/get";
import _truncate from "lodash/truncate";
import React from "react";
import { Card, Label } from "semantic-ui-react";

export const ResultsGridItem = ({ result }) => {
  const metadata = result.metadata;
  return (
    <Card fluid href={_get(result, "links.html", "#")}>
      <Card.Content>
        <Card.Header>{metadata.title}</Card.Header>
        <Card.Description>
          {_truncate(
            metadata.contributors
              .map((contributor) => contributor.name)
              .join("; "),
            { length: 200 }
          )}
        </Card.Description>
      </Card.Content>
      <Card.Content extra>
        {metadata.keywords &&
          metadata.keywords.map((keyword, idx) => (
            <Label key={idx}>{keyword}</Label>
          ))}
      </Card.Content>
    </Card>
  );
};
