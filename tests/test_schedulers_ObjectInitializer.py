from schedulers import ObjectInitializer
from location import Point
from tests.objects import test_schedule
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedulers.ObjectInitializer class
    """
    def setUp(self):
        # Note that the schedule object and all its objects are deep copied
        self.schedule = test_schedule.copy()
        self.object_initializer = ObjectInitializer(self.schedule)

    def test(self):
        # It's important to be precise with object references from here on
        test_appt1 = self.schedule.appts[0]
        test_appt2 = self.schedule.appts[1]
        test_appt3 = self.schedule.appts[2]
        test_interpreter1 = test_appt1.interpreter
        test_interpreter2 = test_appt2.interpreter
        test_interpreter3 = test_appt3.interpreter

        # Note: wrappers are tested when we test the methods they call
        default_appt = self.object_initializer.default_appt

        # init_job
        # Passing an Interpreter object to the jobs dict should return a list
        # of Appointment objects
        self.object_initializer.jobs.pop(test_interpreter1)
        self.object_initializer.init_job(test_interpreter1, test_appt1)
        self.assertEqual(self.object_initializer.jobs[test_interpreter1],
                         [test_appt1])
        self.object_initializer.jobs[test_interpreter1] = [default_appt]

        # populate_objects
        interpreter_lst = [test_interpreter1,
                           test_interpreter2,
                           test_interpreter3]
        languages = {"French", "Spanish"}
        self.assertEqual(self.object_initializer.interpreters,
                         interpreter_lst)
        self.assertEqual(self.object_initializer.languages,
                         languages)

        # test add locs for each point in each appointment
        # Passing Interpreter objects to the locs dict should return a Point
        test_point = self.object_initializer.locs[test_interpreter1]
        locx, locy = test_point.coordinates
        self.assertEqual(self.object_initializer.locs[test_interpreter1],
                         Point(locx, locy))
        test_point = self.object_initializer.locs[test_interpreter2]
        locx, locy = test_point.coordinates
        self.assertEqual(self.object_initializer.locs[test_interpreter2],
                         Point(locx, locy))
        test_point = self.object_initializer.locs[test_interpreter3]
        locx, locy = test_point.coordinates
        self.assertEqual(self.object_initializer.locs[test_interpreter3],
                         Point(locx, locy))

        # test add jobs for each interpreters on each appointment
        # Passing Interpreter objects to the jobs dict should return a list of
        # Appointment objects
        self.assertEqual(self.object_initializer.jobs[test_interpreter1],
                         [default_appt])
        self.assertEqual(self.object_initializer.jobs[test_interpreter2],
                         [default_appt])
        self.assertEqual(self.object_initializer.jobs[test_interpreter3],
                         [default_appt])

        # gen_schedule_dict
        # Note that we are passing an integer dict key not a list index
        self.assertEqual(self.object_initializer.appts_dict[1],
                         test_appt1)
        self.assertEqual(self.object_initializer.appts_dict[2],
                         test_appt2)
        self.assertEqual(self.object_initializer.appts_dict[3],
                         test_appt3)

        # gen_language_dict
        test_dict = {'French': [test_appt3],
                     'Spanish': [test_appt1, test_appt2]}
        self.assertEqual(test_dict, self.object_initializer.language_dict)


if __name__ == '__main__':
    unittest.main()
