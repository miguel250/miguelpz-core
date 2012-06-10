#!/bin/bash

export PYTHONPATH=$PWD
export ENVIRONMENT='Development'
bindip='0.0.0.0:5000'
module='app.config.development:app'

gunicorn -w 2 -c bin/reload.py $module -b $bindip  --log-level=debug 