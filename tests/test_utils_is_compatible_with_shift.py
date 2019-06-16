from utils import is_compatible_with_shift
from tests.objects import (
    test_schedule,
    appt4,
    appt5
)
import unittest
import sys
sys.path.append('..')


class TestFunction(unittest.TestCase):
    """
    Test the utils.is_compatible_with_shift function
    """
    def setUp(self):
        self.schedule = test_schedule
        self.interpreter = test_schedule.interpreters[2]
        self.appt = appt4.copy()
        self.appt2 = appt5.copy()
        
    def test(self):
        # Is compatible tests if the appt start is >= the interpreter's start
        # It also tests if appt finish is <= interpreter's end time
        # To avoid scheduling interpreters at invalid times

        # This test has appt start at 8:45 and appt finish at 10:05
        # This test has interp start at 8:30 and finish at 12:30
        # 8:30 <= 8:45, and 12:30 >= 10:05, so this test should PASS
        is_compatible = is_compatible_with_shift(self.interpreter,
                                                 self.appt)
        self.assertTrue(is_compatible)

        # This test has appt start at 12:45 and appt finish at 13:25
        # This test has interp start at 8:30 and finish at 12:30
        # 8:30 <= 12:45, but 12:30 < 13:25, so this test should FAIL
        is_compatible = is_compatible_with_shift(self.interpreter,
                                                 self.appt2)
        self.assertFalse(is_compatible)


if __name__ == '__main__':
    unittest.main()
