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
        interpreters = self.cls.interpreters

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
        self.cls.time_dict = {}
        time = Time("8:30", TIME_FORMAT)
        self.cls.rev_update_time_dict(time, appts)

        td = self.cls.time_dict["08:00"]
        self.assertEqual(td[0], appts[0])

        td = self.cls.time_dict["08:25"]
        self.assertEqual(td[0], appts[1])

        self.assertNotIn("08:45", self.cls.time_dict.keys())

        # update_valid_choices
        self.cls.appts_to_assign.append(appts[0])
        self.cls.jobs[interpreters[0]] = [self.cls.default_appt]
        self.cls.assign(interpreters[0], appts[0])
        self.cls.update_valid_choices(appts[0].finish, appts)
        self.assertIn(appts[1], self.cls.valid_choices[interpreters[0]])
        self.assertIn(appts[2], self.cls.valid_choices[interpreters[0]])

        # rev_update_valid_choices
        self.cls.rev_update_valid_choices(appts[2].finish, appts)
        self.assertIn(appts[1], self.cls.valid_choices[interpreters[0]])
        self.assertIn(appts[2], self.cls.valid_choices[interpreters[0]])

        # next_valid_choice
        self.cls.appts_to_assign.append(appts[0])
        self.cls.jobs[interpreters[0]] = [self.cls.default_appt]
        last_job = self.cls.get_last_job(interpreters[0])
        time = last_job.finish
        next_appt = self.cls.next_valid_choice(interpreters[0], time)
        self.assertEqual(next_appt, appts[0])


if __name__ == '__main__':
    unittest.main()
