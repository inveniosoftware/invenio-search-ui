..
    This file is part of Invenio.
    Copyright (C) 2015-2023 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 2.8.1 (released 2023-09-22)

- a11y: fix icon roles
- a11y: fix search filter name

Version 2.8.0 (released 2023-09-14)

- search bar: add aria-label
- facets: replace id with aria label
- search bar: fix focus vs click bug and inactive button

Version 2.7.0 (released 2023-09-12)

- facets: convert number to locale, a11y improvements

Version 2.6.1 (released 2023-09-08)

- assets: fix typo on prop name in facets component

Version 2.6.0 (released 2023-08-09)

- pagination: add possibility to show number of results next to it

Version 2.5.0 (released 2023-08-02)

- search dropdown: add flex to button content
- pull translations

Version 2.4.1 (released 2023-04-06)

- control maximum search results

Version 2.4.0 (released 2023-03-02)

- remove deprecated flask-babelex dependency and imports

Version 2.3.0 (released 2023-01-26)

- assets: normalize overridable ids

Version 2.2.0 (released 2022-10-24)

- upgrade react-invenio-forms
- use node 18

Version 2.1.10 (released 2022-09-19)

- add contrib search app components

Version 2.1.9 (released 2022-09-06)

- search app: fix display statement

Version 2.1.8 (released 2022-09-05)

- search app: fix buildUID function resolution

Version 2.1.7 (released 2022-09-05)

- layout: adopt to full width when no facets available
- ux: add label to sort

Version 2.1.6 (released 2022-08-03)

- multi-option searchbar: fix search options resolution

Version 2.1.5 (released 2022-08-02)

- multi-option searchbar: add empty search option

Version 2.1.4 (released 2022-07-29)

- add reusable pagination component

Version 2.1.3 (released 2022-07-08)

- fix mobile pagination
- add multiple option search component

Version 2.1.2 (released 2022-07-01)

- Reduce space between facets and search results in large screens.

Version 2.1.1 (released 2022-05-05)

- Adds responsive sidebar to the search app.

Version 2.1.0 (released 2022-04-05)

- Upgrade react-searchkit version to v2.0.0.

Version 2.0.10 (released 2022-04-05)

- Relax min Python version to 3.6.
- Adds optional wrapper element to the React search app.

Version 2.0.9 (released 2022-03-31)

- Move setup.py to setup.cfg.
- Remove Python 2.7/3.5/3.6 support.
- Upgrade react-searchkit and fixes.

Version 2.0.8 (released 2022-03-25)

- Refactor search app styling.

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
