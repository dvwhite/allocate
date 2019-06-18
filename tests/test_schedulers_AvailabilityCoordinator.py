from schedulers import AvailabilityCoordinator
from tests.objects import test_schedule
import unittest
import sys
sys.path.append('..')


class TestSomething(unittest.TestCase):
    def setUp(self):
        self.schedule = test_schedule.copy()
        self.cls = AvailabilityCoordinator(self.schedule)
        
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()
