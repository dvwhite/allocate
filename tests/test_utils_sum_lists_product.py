from utils import sum_lists_product
import unittest
import sys
sys.path.append('..')


class TestFunction(unittest.TestCase):
    """
    Tests utils.sum_lists_product
    """
    def setUp(self):
        self.lst1 = [1,  2,  3]
        self.lst2 = [4,  5,  6]
        
    def test(self):
        # 0 + 0 = 0
        self.assertEqual(0,  sum_lists_product([],  []))
        # 1 * 0 = 0
        self.assertEqual(0,  sum_lists_product([1],  []))
        # 0 * 1 = 0
        self.assertEqual(0,  sum_lists_product([],  [1]))
        # 1*1 + 2*0 = 1
        self.assertEqual(1,  sum_lists_product([1,  2],  [1]))
        # 1*1 + 2*0 = 1
        self.assertEqual(1,  sum_lists_product([1],  [1,  2]))
        # 1*4 + 2*5 + 3*6 = 32
        result = sum_lists_product(self.lst1,  self.lst2)
        self.assertEqual(result,  (1*4+2*5+3*6))
        self.assertEqual(32, result)


if __name__ == '__main__':
    unittest.main()
