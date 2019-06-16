from utils import enumerate_combinations as ec
import unittest
import sys
sys.path.append('..')


class TestFunction(unittest.TestCase):
    """
    Test utils.enumerate_combinations
    """
    def setUp(self):
        self.lst = [1, 2]
    
    def test(self):
        expected_result3 = set()
        expected_result2 = {(1, 2), (2, 1)}
        expected_result1 = {(2,), (1,)}
        expected_result0 = {()}
        # test is a set
        self.assertIsInstance(ec(self.lst,  2),  set)
        # test output is correct, containing all combinations for n=3, 2, 1, 0
        self.assertEqual(expected_result3,  ec(self.lst,  3))
        self.assertEqual(expected_result2,  ec(self.lst,  2))
        self.assertEqual(expected_result1,  ec(self.lst,  1))
        self.assertEqual(expected_result0,  ec(self.lst,  0))


if __name__ == '__main__':
    unittest.main()
