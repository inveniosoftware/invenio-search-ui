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
flask collect -v
flask webpack buildall

# Create the database
flask db init
flask db create

# Initialize indices
flask index init
flask index queue init
