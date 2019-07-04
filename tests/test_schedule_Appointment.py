from schedule import Appointment
from tests.objects import (
    appt1,
    appt2,
    appt3
)
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
        self.assertTrue(self.appt.is_compatible(self.appt))
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

        # __str__
        appt_str = ("1|08:00|10|08:10|" +
                    "Joe Spanish|('East Wing', 'Emergency Room')" +
                    "|100|Dr. John|Jose Gomez|15")
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
