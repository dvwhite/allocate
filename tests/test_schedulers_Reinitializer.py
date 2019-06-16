from schedulers import Reinitializer
from tests.objects import test_schedule
from location import Point
import collections
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedulers.Reinitializer class
    """
    def setUp(self):
        self.schedule = test_schedule.copy()
        self.reinitializer = Reinitializer(self.schedule)
        
    def test(self):
        # _reset_attributes
        self.reinitializer._reset_attributes()
        self.assertEqual(0, self.reinitializer.impact)
        self.assertEqual(0, self.reinitializer.schedule.impact)

        # _reset_data_structures
        self.reinitializer._reset_data_structures()
        self.assertEqual(self.reinitializer.time_dict,
                         collections.defaultdict(list))
        self.assertEqual(self.reinitializer.valid_choices,
                         collections.defaultdict(list))
        self.assertEqual(self.reinitializer.jobs, {})
        self.assertEqual(self.reinitializer.locs, {})
        self.assertEqual(self.reinitializer.schedule_dict, {})
        self.assertEqual(self.reinitializer.schedule_paths, [])
        self.assertEqual(self.reinitializer.best_paths, {})

        # _reset_objects
        self.reinitializer._reset_objects()
        all_empty_str = all([True for x in self.reinitializer.interpreters
                             if x == ""])
        all_in_locs = all([True for x in self.reinitializer.interpreters
                           if x in self.reinitializer.locs.keys()])
        all_in_jobs = all([True for x in self.reinitializer.interpreters
                           if x in self.reinitializer.jobs.keys()])
        all_locs_zeroed = all([True for (x, y) in
                               self.reinitializer.locs.items()
                               if y == Point(0, 0)])
        all_jobs_default = all([True for (x, y) in
                                self.reinitializer.jobs.items()
                                if y == self.reinitializer.default_appt])
        self.assertTrue(all_empty_str)
        self.assertTrue(all_in_locs)
        self.assertTrue(all_in_jobs)
        self.assertTrue(all_locs_zeroed)
        self.assertTrue(all_jobs_default)


if __name__ == '__main__':
    unittest.main()
