import os
import sys
import inspect
import unittest

def suite():
    suite = unittest.TestSuite()
    root = os.getcwd()
    path = os.path.join(root, "app/tests")

    for all_test_suite in unittest.defaultTestLoader.discover(path,pattern='*_tests.py'):
       for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())