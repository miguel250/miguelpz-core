#!/bin/bash

export PYTHONPATH='.'
export ENVIRONMENT='production'
bindip='127.0.0.1:5000'
module='app.config.run:app'

gunicorn -w 4 -b $bindip --log-level=info  --log-file=logs/gunicorn.log $module
#gunicorn -w 4  -b $bindip  --log-level=info  $module