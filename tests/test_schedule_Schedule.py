from schedule import (
    Schedule,
)
from tests.objects import (
    interpreter1,
    interpreter2,
    appt1,
    appt2,
    appt3,
    patient1,
    patient2
)
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedule.Schedule class
    """
    def setUp(self):
        self.interpreters = [interpreter1, interpreter2]
        self.appts = [appt1, appt2, appt3]
        self.patients = [patient1, patient2]
        self.sched = Schedule(appts=self.appts,
                              interpreters=self.interpreters)
        
    def test(self):
        # calc_impact
        self.assertEqual(self.sched.calc_impact(), 150)

        # copy
        copied = self.sched.copy()
        self.assertIsInstance(copied, Schedule)
        self.assertEqual(copied, self.sched)
        self.assertTrue(appt1 in copied.appts)
        self.assertTrue(appt2 in copied.appts)
        self.assertTrue(appt3 in copied.appts)

        # gen_intervals
        generated = self.sched.gen_intervals()
        expected = {"i": [1, 2, 3],
                    "s": ["08:00", "08:25", "08:45"],
                    "f": ["08:10", "09:05", "09:25"],
                    "v": [100, 30, 20],
                    "x": [3, 0, 4],
                    "y": [4, 0, -4]}
        self.assertEqual(generated, expected)

        # brief
        brief_str_appt1 = (str(appt1.idnum) + "|" +
                           str(appt1.start) + "|" +
                           str(appt1.finish) + "|" +
                           str(appt1.patient) + "|" +
                           str(appt1.location.coordinates) + "|" +
                           str(appt1.interpreter))

        brief_str_appt2 = (str(appt2.idnum) + "|" +
                           str(appt2.start) + "|" +
                           str(appt2.finish) + "|" +
                           str(appt2.patient) + "|" +
                           str(appt2.location.coordinates) + "|" +
                           str(appt2.interpreter))
        
        brief_str_appt3 = (str(appt3.idnum) + "|" +
                           str(appt3.start) + "|" +
                           str(appt3.finish) + "|" +
                           str(appt3.patient) + "|" +
                           str(appt3.location.coordinates) + "|" +
                           str(appt3.interpreter))

        brief_str = (brief_str_appt1 + "\n" +
                     brief_str_appt2 + "\n" +
                     brief_str_appt3 + "\n")

        self.assertEqual(self.sched.brief(), brief_str)

        # __eq__
        copied_schedule = self.sched.copy()
        self.assertEqual(self.sched, copied_schedule)

        # __ne__
        copied_schedule = self.sched.copy()
        copied_schedule.appts[0].idnum = 100
        self.assertNotEqual(self.sched, copied_schedule)


if __name__ == '__main__':
    unittest.main()
