// This file is part of invenio-search-ui
// Copyright (C) 2021 Graz University of Technology.
//
// invenio-search-ui is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

const { writeFileSync } = require("fs");
const packageJson = require("../package");

const { languages } = packageJson.config;
if ("lang" === process.argv[2]) {
  const addedLang = process.argv[3];
  languages.push(addedLang);
  packageJson.config.languages = [...new Set(languages)];
  writeFileSync(`package.json`, JSON.stringify(packageJson, null, 2));
} else {
  console.error(
    "Error:Please provide a language by running `npm run init_catalog lang <lang>`"
  );
}
