from utils import calc_arrival
from tests.objects import test_schedule
import unittest
import sys
sys.path.append('..')


class TestFunction(unittest.TestCase):
    """
    Test the utils.calc_arrival function
    """
    def setUp(self):
        self.appts = test_schedule
        
    def test(self):
        dist = test_schedule.appts[0]


if __name__ == '__main__':
    unittest.main()
