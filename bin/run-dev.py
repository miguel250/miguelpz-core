#!/usr/bin/env python
import sys, os
from app.config.run import run
os.environ['ENVIRONMENT'] = 'development'

if __name__ == '__main__':
    run.run()