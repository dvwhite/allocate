from schedulers import BruteForceDP
from tests.objects import test_schedule
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the BruteForceDP class
    """
    def setUp(self):
        self.schedule = test_schedule.copy()
        self.cls = BruteForceDP(self.schedule)
        
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()
