from ScheduleSim import typedef
import unittest
import sys
sys.path.append('..')


class DummyClass(object):
    """
    A dummy class for testing purposes; no methods or properties necessary
    """
    def __init__(self):
        pass


class TestFunction(unittest.TestCase):
    """
    Test the utils.typedef function
    """
    def setUp(self):
        self.obj = int(2.4)
        self.obj2 = DummyClass()
       
    def test(self):
        self.assertEqual(self.obj, 2)
        self.assertEqual(typedef(self.obj),  "int")
        self.assertEqual(typedef(self.obj2),  "DummyClass")

        
if __name__ == '__main__':
    unittest.main()
