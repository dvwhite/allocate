from schedule import Appointment
from tests.objects import (
    appt1,
    appt2,
    appt3,
)
from constants import TIME_FORMAT
from utils import Time
import bisect
import copy
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedule.Appointment class
    """
    def setUp(self):
        self.appt = appt1
        self.appt2 = appt2
        
    def test(self):
        # copy
        copied = self.appt.copy()
        self.assertIsInstance(copied,  Appointment)
        self.assertEqual(self.appt, copied)

        # is_compatible
        self.assertTrue(self.appt.is_compatible(self.appt2))

        # distance_from
        self.assertEqual(self.appt.distance_from(self.appt2), 5)

        # brief
        brief_str_appt = (str(self.appt.idnum) + "|" +
                          str(self.appt.start) + "|" +
                          str(self.appt.finish) + "|" +
                          str(self.appt.patient) + "|" +
                          str(self.appt.location.coordinates) + "|" +
                          str(self.appt.interpreter))
        actual = self.appt.brief()
        self.assertEqual(brief_str_appt, actual)

        # calc_prior
        others = [appt1, appt2, appt3]
        appt_to_test = appt3
        appt_idx = others.index(appt_to_test)
        self.assertEqual(2, appt_idx)

        start = [interval.start for interval in others]
        self.assertEqual([Time("8:00", TIME_FORMAT),
                          Time("8:25", TIME_FORMAT),
                          Time("8:45", TIME_FORMAT)], start)

        finish = [interval.finish for interval in others]
        self.assertEqual([Time("8:10", TIME_FORMAT),
                          Time("9:05", TIME_FORMAT),
                          Time("9:25", TIME_FORMAT)], finish)

        # overlapping marks the next interval that would overlap,
        # meaning that interval a.finish would be > than appt_to_test.start
        overlapping = bisect.bisect(finish, start[appt_idx])
        self.assertEqual(1, overlapping)
        self.assertEqual(Time("9:05", TIME_FORMAT),
                         finish[overlapping])
        # appt_to_test.start. In order to satisfy the condition,
        # we need a.finish < appt_to_test.start, so we exclude
        # the appts that aren't compatible
        compatible_copy = copy.deepcopy(others[:overlapping])
        self.assertEqual([appt1], compatible_copy)

        # We sort the indices of compatible appts in reverse order
        # and test them for compatibility, until one is found.
        # Doing so in reverse order ensures the compatible appt is
        # the rightmost compatible appt
        compatible_idx = [others.index(other) for other in compatible_copy]
        compatible_idx.sort(reverse=True)
        self.assertEqual([0], compatible_idx)
        rightmost_compatible_appt = others[compatible_idx[-1]]
        self.assertTrue(rightmost_compatible_appt.is_compatible(appt_to_test))
        self.assertEqual(appt1, appt3.calc_prior(others))

        # get_prior_num
        long_appt = Appointment(299999, "7:00", 360, appt1.patient,
                                appt1.location, 10000, appt1.provider, "")
        short_appt = Appointment(1000, "13:05", 1, appt1.patient,
                                 appt1.location, 1000, appt1.provider, "")

        others += [long_appt, short_appt]
        self.assertEqual(others, [appt1, appt2, appt3, long_appt, short_appt])
        prior = short_appt.calc_prior(others)
        prior_idx = others.index(prior)
        self.assertEqual(long_appt, prior)
        self.assertEqual(prior_idx, 3)
        self.assertIsNotNone(prior)
        self.assertEqual(prior_idx, short_appt.get_prior_num(others))

        # __str__
        appt_str = ("1|08:00|10|08:10|" +
                    "Joe Spanish|('East Wing', 'Emergency Room')" +
                    "|100|Dr. John|Jose Gomez|0")
        self.assertEqual(str(self.appt), appt_str)

        # __hash__
        expected_hash = id(self.appt)
        actual_hash = self.appt.__hash__()
        self.assertEqual(expected_hash, actual_hash)

        # __eq__
        copied_appt = self.appt.copy()
        copied_appt.__dict__ = self.appt.__dict__
        self.assertEqual(self.appt, copied_appt)

        # __ne__
        copied_appt = self.appt.copy()
        copied_appt.idnum = 100
        self.assertNotEqual(self.appt, copied_appt)

        # __lt__
        self.assertLess(appt1, appt2)
        self.assertLess(appt2, appt3)
        appt_lst1 = [appt3, appt2, appt1]
        appt_lst2 = [appt2, appt3, appt1]
        appt_lst1.sort()
        appt_lst2.sort()
        self.assertEqual(appt_lst1[0], appt1)
        self.assertEqual(appt_lst1[-1], appt3)
        self.assertEqual(appt_lst2[0], appt1)
        self.assertEqual(appt_lst2[-1], appt3)


if __name__ == '__main__':
    unittest.main()
