#!/bin/sh

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# clean environment
[ -e "$DIR/static" ] && rm $DIR/static/ -Rf

# Clean the indices
flask index destroy --yes-i-know

# Clean the database
flask db destroy --yes-i-know
