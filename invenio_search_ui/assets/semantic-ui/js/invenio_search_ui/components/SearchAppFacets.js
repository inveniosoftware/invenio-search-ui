/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import React from "react";
import { BucketAggregation, RangeFacet, buildUID } from "react-searchkit";
import Overridable from "react-overridable";

export const SearchAppFacets = ({ aggs, appName }) => {
  const buildOverridableUID = (element) => buildUID(element, "", appName);
  return (
    <Overridable
      id={buildOverridableUID("SearchApp.facets", "", appName)}
      aggs={aggs}
      appName={appName}
    >
      <>
        {aggs.map((agg) =>
          agg.type === "date" ? (
            <RangeFacet
              key={agg.title}
              title={agg.title}
              agg={agg}
              rangeSeparator={agg.separator || ".."}
            />
          ) : (
            <BucketAggregation key={agg.title} title={agg.title} agg={agg} />
          ),
        )}
      </>
    </Overridable>
  );
};
