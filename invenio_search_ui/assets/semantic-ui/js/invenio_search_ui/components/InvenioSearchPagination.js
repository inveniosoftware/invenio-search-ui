/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-FileCopyrightText: 2025 KTH Royal Institute of Technology.
 * SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import { Trans } from "react-i18next";
import { i18next } from "@translations/invenio_search_ui/i18next";
import { Pagination, ResultsPerPage, Count } from "react-searchkit";
import { Grid } from "semantic-ui-react";

export const InvenioSearchPagination = ({ paginationOptions, total }) => {
  const { maxTotalResults, resultsPerPage } = paginationOptions;
  return (
    <Grid.Row verticalAlign="middle">
      <Grid.Column className="computer tablet only" width={4}>
        {total && (
          <Count
            label={() => (
              <Trans
                i18n={i18next}
                defaults={"<bold>{{count}}</bold> results found"}
                values={{ count: total.toLocaleString("en-US") }}
                components={{ bold: <b /> }}
                count={total}
              />
            )}
          />
        )}
      </Grid.Column>
      <Grid.Column className="computer tablet only" width={8} textAlign="center">
        <Pagination
          options={{
            size: "mini",
            showFirst: false,
            showLast: false,
            maxTotalResults,
          }}
        />
      </Grid.Column>
      <Grid.Column className="mobile only" width={16} textAlign="center">
        <Pagination
          options={{
            boundaryRangeCount: 0,
            showFirst: false,
            showLast: false,
            maxTotalResults,
          }}
        />
      </Grid.Column>
      <Grid.Column className="computer tablet only " textAlign="right" width={4}>
        <ResultsPerPage
          values={resultsPerPage}
          label={(cmp) => (
            <Trans
              i18n={i18next}
              defaults={"<pageSize/> results per page"}
              components={{ pageSize: cmp }}
            />
          )}
        />
      </Grid.Column>
      <Grid.Column className="mobile only rel-mt-2" textAlign="center" width={16}>
        {total && (
          <Count
            label={() => (
              <span className="rel-mr-2">
                <Trans
                  i18n={i18next}
                  defaults={"<bold>{{count}}</bold> results found"}
                  values={{ count: total.toLocaleString("en-US") }}
                  components={{ bold: <b /> }}
                  count={total}
                />
              </span>
            )}
          />
        )}
        <ResultsPerPage
          values={resultsPerPage}
          label={(cmp) => (
            <Trans
              i18n={i18next}
              defaults={"<pageSize/> results per page"}
              components={{ pageSize: cmp }}
            />
          )}
        />
      </Grid.Column>
    </Grid.Row>
  );
};
