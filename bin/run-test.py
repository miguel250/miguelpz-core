#!/usr/bin/env python
import sys, os
from app.tests import main
os.environ['ENVIRONMENT'] = 'testing'
main()