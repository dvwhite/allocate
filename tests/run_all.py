import os
import unittest

test_folder = os.path.dirname(os.path.realpath(__file__))

loader = unittest.TestLoader()
suite = loader.discover(test_folder)
runner = unittest.TextTestRunner()
runner.run(suite)
