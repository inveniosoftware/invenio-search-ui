..
    This file is part of Invenio.
    Copyright (C) 2015-2022 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 2.0.7 (released 2022-03-16)

- Add helpers to build search pages with React-SearchKit.

Version 2.0.6 (released 2022-02-28)

- Fix web accessibility issue.

Version 2.0.5 (released 2022-02-11)

- Upgrade react-overridable dependency.

Version 2.0.4 (released 2022-02-02)

- Add namespace based on `config.appId` passed from DOM.
- Enable multiple search application support. Introduces a new parameter in
  `utils.createSearchAppInit(...)` called `multi` that allows users to override
  each application's components using `appId` as a prefix.
- Bump semantic-ui-react to latest release
- Adds `@semantic-ui-react/css-patch` because of https://github.com/Semantic-Org/Semantic-UI/issues/7073

Version 2.0.2 (released 2021-02-22)

- Pass search config in overridable `SearchApp.layout`

Version 2.0.1 (released 2021-02-10)

- Make sortOptions available when overriding Results component
- Align pagination to center

Version 2.0.0 (released 2020-12-10)

- SearchApp refactoring
    - Standardize and document configuration
    - Improve reusability and customization for other modules
    - Split into smaller overridable components
    - Make default searchbar overridable
    - Make sort configurable
    - Add configuration to disable sort order
    - Pass backend agg to aggregation component
- Bump React-SearchKit JS version.
- Adds React-SearchKit JS application for use with Semantic UI theme.
- Adapt to latest React-SearchKit changes.
- Migrate CI to GitHub actions.
- Fixes metadata path in AngularJS template.
- Moves AngularJS files in correct path.

Version 1.2.0 (released 2020-03-13)

- Drops support for Python 2.7
- Changes Flask dependency to centrally managed by invenio-base

Version 1.1.1 (released 2018-11-12)

- Includes missing assets for AMD build.

Version 1.1.0 (released 2018-11-06)

- Introduces Webpack support.

Version 1.0.1 (released 2018-03-23)

- facets: fix facets templates.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
