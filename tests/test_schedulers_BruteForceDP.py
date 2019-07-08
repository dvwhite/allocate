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
        appt_weights = {0: 0, 1: 215, 2: 215, 3: 215, 4: 215, 5: 215,
                        6: 430, 7: 430, 8: 430, 9: 430, 10: 430, 11: 645,
                        12: 645, 13: 645, 14: 645, 15: 645, 16: 645,
                        17: 645, 18: 860, 19: 860, 20: 975, 21: 1065,
                        22: 1065, 23: 1072, 24: 1075, 25: 1290, 26: 1290,
                        27: 1385, 28: 1502, 29: 1502, 30: 1502, 31: 1505,
                        32: 1505, 33: 1597, 34: 1597, 35: 1597, 36: 1600,
                        37: 1607, 38: 1720, 39: 1720, 40: 1720, 41: 1720,
                        42: 1720, 43: 1720, 44: 1795, 45: 1915, 46: 1990,
                        47: 2010, 48: 2010, 49: 2222}
        self.assertEqual(appt_weights, self.cls.appt_weights)

        # compute_optimal
        # in bf_ids_dict, the key means that the bf algorithm analyzed
        # self.schedule.appts[:key + 1], meaning at key 0 there was only
        # one appointment analyzed, at key 1, there were two analyzed,
        # at key three, 0-2 indices were included in the analysis,
        # and this continues for as many indices as in
        # range(len(self.schedule.appts)),
        bf_ids_dict = {1: [2],
                       2: [2],
                       3: [2],
                       4: [2],
                       5: [2],
                       6: [2, 7],
                       7: [2, 7],
                       8: [2, 7],
                       9: [2, 7],
                       10: [2, 7],
                       11: [2, 7, 12],
                       12: [2, 7, 12],
                       13: [2, 7, 12],
                       14: [2, 7, 12],
                       15: [2, 7, 12],
                       16: [2, 7, 12],
                       17: [2, 7, 12],
                       18: [2, 7, 12, 19],
                       19: [2, 7, 12, 19],
                       20: [2, 7, 12, 19, 21],
                       21: [2, 7, 12, 19, 22],
                       22: [2, 7, 12, 19, 22],
                       23: [2, 7, 12, 19, 24],
                       24: [2, 7, 12, 19, 25],
                       25: [2, 7, 12, 19, 25, 26],
                       26: [2, 7, 12, 19, 25, 26],
                       27: [2, 7, 12, 19, 25, 26, 28],
                       28: [2, 7, 12, 19, 25, 26, 29],
                       29: [2, 7, 12, 19, 25, 26, 29],
                       30: [2, 7, 12, 19, 25, 26, 29],
                       31: [2, 7, 12, 19, 25, 26, 32],
                       32: [2, 7, 12, 19, 25, 26, 32],
                       33: [2, 7, 12, 19, 25, 26, 28, 34],
                       34: [2, 7, 12, 19, 25, 26, 28, 34],
                       35: [2, 7, 12, 19, 25, 26, 28, 34],
                       36: [2, 7, 12, 19, 25, 26, 28, 37],
                       37: [2, 7, 12, 19, 25, 26, 28, 37],
                       38: [2, 7, 12, 19, 25, 26, 33, 39],
                       39: [2, 7, 12, 19, 25, 26, 33, 39],
                       40: [2, 7, 12, 19, 25, 26, 33, 39],
                       41: [2, 7, 12, 19, 25, 26, 33, 39],
                       42: [2, 7, 12, 19, 25, 26, 33, 39],
                       43: [2, 7, 12, 19, 25, 26, 33, 39],
                       44: [2, 7, 12, 19, 25, 26, 33, 43, 45],
                       45: [2, 7, 12, 19, 25, 26, 33, 43, 46],
                       46: [2, 7, 12, 19, 25, 26, 33, 43, 45, 47],
                       47: [2, 7, 12, 19, 25, 26, 33, 43, 45, 48],
                       48: [2, 7, 12, 19, 25, 26, 33, 43, 45, 48],
                       49: [2, 7, 12, 19, 25, 26, 33, 43, 45, 48]}

        def test_num(num):
            appts = [int(idnum) for idnum in
                     self.cls.compute_optimal(num).split(", ")]
            appts.sort()
            appts.pop(0)

            co_ids = [self.cls.schedule.appts[idx].idnum for idx in appts]
            bf_ids = bf_ids_dict[num]

            bf_sum = sum(bf_appt.priority for bf_appt in
                         self.cls.get_jobs_with_ids(bf_ids))
            co_sum = sum([co_appt.priority for co_appt in
                          self.cls.get_jobs_with_ids(co_ids)])
            self.assertLessEqual(bf_sum, co_sum)

        # Try an increasing index number

        # First, reset the class instance
        self.schedule = bf_test_schedule.copy()
        self.cls = BruteForceDP(self.schedule)

        # 1
        test_num(1)

        # 2
        test_num(2)

        # 3
        test_num(3)

        # 4
        test_num(4)

        # 5
        test_num(5)

        # 6
        test_num(6)

        # 7
        test_num(7)

        # 8
        test_num(8)

        # 9
        test_num(9)

        # 10
        test_num(10)

        # 11
        test_num(11)

        # 12
        test_num(12)

        # 13
        test_num(13)

        # 14
        test_num(14)

        # 15
        test_num(15)

        # 16
        test_num(16)

        # 17
        test_num(17)

        # 18
        test_num(18)

        # 19
        test_num(19)

        # 20
        test_num(20)

        # 21
        test_num(21)

        # 22
        test_num(22)

        # 23
        test_num(23)

        # 24
        test_num(24)

        # 25
        test_num(25)

        # 26
        test_num(26)

        # 27
        test_num(27)

        # 28
        test_num(28)

        # 29
        test_num(29)

        # 30
        test_num(30)

        # 31
        test_num(31)

        # 32
        test_num(32)

        # 33
        test_num(33)

        # 34
        test_num(34)

        # 35
        test_num(35)

        # 36
        test_num(36)

        # 37
        test_num(37)

        # 38
        test_num(38)

        # 39
        test_num(39)

        # 40
        test_num(40)

        # 41
        test_num(41)

        # 42
        test_num(42)

        # 43
        test_num(43)

        # 44
        test_num(44)

        # 45
        test_num(45)

        # 46
        test_num(46)

        # 47
        test_num(47)

        # 48
        test_num(48)

        # 49
        test_num(49)

        # print_schedule
        pass

        # gen_optimal
        pass

        # create_cached_assignment
        pass


if __name__ == '__main__':
    unittest.main()
