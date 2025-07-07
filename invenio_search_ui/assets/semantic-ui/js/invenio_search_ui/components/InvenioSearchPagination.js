// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2025 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { i18next } from "@translations/invenio_search_ui/i18next";
import { Pagination, ResultsPerPage, Count } from "react-searchkit";
import { Grid } from "semantic-ui-react";

export const InvenioSearchPagination = ({ paginationOptions, total }) => {
  const { maxTotalResults, resultsPerPage } = paginationOptions;
  return (
    <Grid.Row verticalAlign="middle">
      <Grid.Column className="computer tablet only" width={4}>
        {total && <Count
          label={() => (
            <>
              <b>{total.toLocaleString("en-US")}</b> {i18next.t("results found")}
            </>
          )}
        />}
      </Grid.Column>
      <Grid.Column
        className="computer tablet only"
        width={8}
        textAlign="center"
      >
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
      <Grid.Column
        className="computer tablet only "
        textAlign="right"
        width={4}
      >
        <ResultsPerPage
          values={resultsPerPage}
          label={(cmp) => (
            <>
              {cmp} {i18next.t("results per page")}
            </>
          )}
        />
      </Grid.Column>
      <Grid.Column className="mobile only rel-mt-2" textAlign="center" width={16}>
        {total && <Count
          label={() => (
            <span className="rel-mr-2">
              <>
                <b>{total.toLocaleString("en-US")}</b> {i18next.t("results found")}
              </>
            </span>
          )}
        />}
        <ResultsPerPage
          values={resultsPerPage}
          label={(cmp) => (
            <>
              {cmp} {i18next.t("results per page")}
            </>
          )}
        />
      </Grid.Column>
    </Grid.Row>
  );
};
