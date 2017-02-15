#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# Install specific dependencies
pip install -r requirements.txt

# Preapare all static files:
npm install -g node-sass clean-css clean-css-cli requirejs uglify-js
flask npm
cd static ; npm install ; cd ..
flask collect -v
flask assets build

# Create the database
flask db init
flask db create

# Initialize indices
flask index init
flask index queue init
