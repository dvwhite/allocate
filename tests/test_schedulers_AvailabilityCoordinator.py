from schedulers import AvailabilityCoordinator
from tests.objects import test_schedule
from utils import Time
from constants import TIME_FORMAT
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedulers.AvailabilityCoordinator class
    """
    def setUp(self):
        self.schedule = test_schedule.copy()
        self.cls = AvailabilityCoordinator(self.schedule)
        
    def test(self):
        appts = self.schedule.appts

        # update_time_dict
        time = Time("8:00", TIME_FORMAT)
        self.cls.update_time_dict(time, appts)

        td = self.cls.time_dict["08:00"]
        self.assertEqual(td[0], appts[0])

        td = self.cls.time_dict["08:25"]
        self.assertEqual(td[0], appts[1])

        td = self.cls.time_dict["08:45"]
        self.assertEqual(td[0], appts[2])

        # rev_update_time_dict
        pass

        # update_valid_choices
        pass

        # rev_update_valid_choices
        pass

        # next_valid_choice
        pass


if __name__ == '__main__':
    unittest.main()
