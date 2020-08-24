/*
 * This file is part of Invenio.
 * Copyright (C) 2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import defaultComponents from "./defaultComponents";
import { createSearchAppInit } from "./util";

// Create and autoinitialize the search app
createSearchAppInit(defaultComponents);
