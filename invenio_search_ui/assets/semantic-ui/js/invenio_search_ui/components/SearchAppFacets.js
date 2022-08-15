/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import {
  BucketAggregation,
} from "react-searchkit";
import Overridable, {
} from "react-overridable";

export const SearchAppFacets = ({ aggs, buildUID, appName }) => {

  return (
    <Overridable id={buildUID("SearchApp.facets", "", appName)} aggs={aggs}>
      <>
        {aggs.map((agg) => (
          <BucketAggregation key={agg.title} title={agg.title} agg={agg.agg} />
        ))}
      </>
    </Overridable>
  );
};

