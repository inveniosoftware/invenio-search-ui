#!/bin/sh

# clean environment
[ -e "app.db" ] && rm app.db
[ -e "static" ] && rm static -Rf
[ -e "instance" ] && rm instance -Rf

export FLASK_APP=app.py

# Install specific dependencies
pip install -r requirements.txt

# Preapare all static files:
npm install -g node-sass clean-css requirejs uglify-js
flask npm
cd static ; npm install ; cd ..
flask collect -v
flask assets build
mkdir instance

# Create demo records
flask db init
flask db create
flask index init
flask fixtures records

# Start the server
flask run --debugger -h 0.0.0.0 -p 5000
