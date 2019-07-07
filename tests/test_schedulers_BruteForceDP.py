from schedulers import BruteForceDP
from tests.objects import bf_test_schedule
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the BruteForceDP class
    """
    def setUp(self):
        self.schedule = bf_test_schedule.copy()
        self.cls = BruteForceDP(self.schedule)
        
    def test(self):

        # _cache_original_weights
        weights = {1: 85, 2: 215, 3: 85, 4: 213, 5: 215, 6: 115, 7: 215,
                   8: 115, 9: 212, 10: 105, 11: 215, 12: 215, 13: 95,
                   14: 115, 15: 125, 16: 215, 17: 205, 18: 85, 19: 215,
                   20: 115, 21: 115, 22: 205, 23: 205, 24: 212, 25: 215,
                   26: 215, 27: 115, 28: 95, 29: 212, 30: 205, 31: 195,
                   32: 215, 33: 215, 34: 212, 35: 195, 36: 115, 37: 215,
                   38: 105, 39: 215, 40: 85, 41: 85, 42: 85, 43: 215,
                   44: 212, 45: 75, 46: 195, 47: 195, 48: 215, 49: 215,
                   50: 212}
        self.assertEqual(weights, self.cls.orig_weights)

        # reset_weights
        for appt in self.schedule.appts:
            appt.priority = 0
        self.assertEqual(0, sum([appt.priority for appt in
                                 self.schedule.appts]))
        self.cls.reset_weights()
        for appt in self.schedule.appts:
            idx = appt.idnum
            self.assertEqual(appt.priority, weights[idx])

        # update_weights
        interpreter = self.schedule.interpreters[0]
        interpreter.assignments = {"Central Hospital": 3,
                                   "West Wing": 2,
                                   "East Wing": 3}
        self.cls.update_weights(interpreter)
        for appt in self.schedule.appts:
            idx = appt.idnum
            if appt.location.building == "West Wing":
                self.assertEqual(appt.priority, 2 * weights[idx])
            else:
                self.assertEqual(appt.priority, 3 * weights[idx])

        # calculate_weights
        pass

        # compute_optimal
        pass

        # print_schedule
        pass

        # gen_optimal
        pass

        # create_cached_assignment
        pass


if __name__ == '__main__':
    unittest.main()
