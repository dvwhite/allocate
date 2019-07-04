from schedulers import JobSupervisor
from location import Point
from tests.objects import (
    test_schedule,
    appt4,
    appt5,
    appt6,
    appt7
)
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the schedulers.JobSupervisor class
    """
    def setUp(self):
        self.schedule = test_schedule.copy()
        self.cls = JobSupervisor(self.schedule)
        self.interpreter = self.schedule.interpreters[2]
        self.appt = appt4.copy()
        self.appt2 = appt5.copy()

    def test(self):
        appts = self.cls.schedule.appts
        interpreters = self.cls.interpreters

        # get_job_with_id
        # Returns an appointment from self.appt_dict at index id
        # Due to overlap with the id builtin, the variable name is job_id
        #
        # This test indexes a pre-made test object and assert
        # equality to the index as the first test condition
        # If this test fails then the test object has been changed
        self.assertEqual(appts[0].idnum, 1)
        self.assertEqual(self.cls.get_job_with_id(1), appts[0])

        # get_jobs_with_ids
        # Calls get_job_with_id on each id and returns a list of appts found
        # Asserting object equality by index ensures no mutation interference
        ids1 = [1, 2, 3]
        ids2 = [1, 2, 7]
        ids3 = [5, 6, 7]
        self.assertEqual(appts[0].idnum, ids1[0])
        self.assertEqual(appts[1].idnum, ids1[1])
        self.assertEqual(appts[2].idnum, ids1[2])
        test_list = self.cls.get_jobs_with_ids(ids1)
        self.assertEqual([appts[0], appts[1], appts[2]], test_list)

        self.assertEqual(appts[0].idnum, ids1[0])
        self.assertEqual(appts[1].idnum, ids1[1])
        test_list = self.cls.get_jobs_with_ids(ids2)
        self.assertEqual([appts[0], appts[1]], test_list)

        test_list = self.cls.get_jobs_with_ids(ids3)
        self.assertEqual([], test_list)

        # get_last_job
        job = self.cls.get_last_job(interpreters[0])
        self.assertEqual(job, appts[0])

        job = self.cls.get_last_job(interpreters[1])
        self.assertEqual(job, appts[1])

        job = self.cls.get_last_job(interpreters[2])
        self.assertEqual(job, appts[2])

        # get_jobs
        jobs = self.cls.get_jobs(interpreters[0])
        self.assertEqual(jobs, [self.cls.default_appt,
                                appts[0]])

        jobs = self.cls.get_jobs(interpreters[1])
        self.assertEqual(jobs, [self.cls.default_appt,
                                appts[1]])

        jobs = self.cls.get_jobs(interpreters[2])
        self.assertEqual(jobs, [self.cls.default_appt,
                                appts[2]])

        # add_job
        self.cls.add_job(interpreters[2], appt4)
        jobs = self.cls.get_jobs(interpreters[2])
        self.assertEqual(jobs, [self.cls.default_appt,
                                appts[2],
                                appt4])

        # Is compatible tests if the appt start is >= the interpreter's start
        # It also tests if appt finish is <= interpreter's end time
        # To avoid scheduling interpreters at invalid times

        # This test has appt start at 8:45 and appt finish at 10:05
        # This test has interp start at 8:30 and finish at 12:30
        # 8:30 <= 8:45, and 12:30 >= 10:05, so this test should PASS
        is_compatible = self.cls.is_appt_in_shift(self.interpreter,
                                                          self.appt)
        self.assertTrue(is_compatible)

        # This test has appt start at 12:45 and appt finish at 13:25
        # This test has interp start at 8:30 and finish at 12:30
        # 8:30 <= 12:45, but 12:30 < 13:25, so this test should FAIL
        is_compatible = self.cls.is_appt_in_shift(self.interpreter,
                                                          self.appt2)
        self.assertFalse(is_compatible)

        # calc_impact
        self.assertEqual(self.cls.calc_impact(), 150)

        # can_assign
        self.assertTrue(self.cls.can_assign(interpreters[0],
                                                       appts[0],
                                                       appts[1]))
        self.assertFalse(self.cls.can_assign(interpreters[0],
                                                        appts[0],
                                                        appts[0]))

        # can_insert_job
        self.cls.appts_to_assign.append(appt6)
        self.assertTrue(self.cls.can_insert_job(interpreters[0],
                                                           appt6))
        self.cls.assign(interpreters[0], appt6)
        self.assertFalse(self.cls.can_insert_job(interpreters[0],
                                                            appt7))

        # assign
        # save existing assigned staff before reset
        interpreter = appts[0].interpreter
        # reset objects
        appts[0].interpreter = ""
        self.cls.jobs[interpreter].remove(appts[0])
        self.cls.move_to(interpreter, Point(0, 0))
        self.cls.appts_to_assign.append(appts[0])

        # assign the interpreter to the appointment
        self.cls.assign(interpreter, appts[0])
        self.assertEqual(appts[0].interpreter, interpreter)
        self.assertIn(appts[0], self.cls.jobs[interpreter])
        self.assertEqual(Point(*appts[0].location.coordinates),
                         self.cls.locs[interpreter])

        # group_assign
        # reset appts[0]
        self.cls.jobs[interpreter].remove(appts[0])
        self.cls.move_to(interpreter, Point(0, 0))
        self.cls.appts_to_assign.append(appts[0])
        # reset appt6
        self.cls.jobs[interpreter].remove(appt6)
        self.cls.move_to(interpreter, Point(0, 0))
        self.cls.appts_to_assign.append(appt6)

        # create jobs and call the method under test
        jobs = [appts[0], appt6]
        self.cls.group_assign(interpreter, jobs)
        # check for appts[0] assignment
        self.assertEqual(appts[0].interpreter, interpreter)
        self.assertIn(appts[0], self.cls.jobs[interpreter])
        # check for appt6 assignment
        self.assertEqual(appt6.interpreter, interpreter)
        self.assertIn(appt6, self.cls.jobs[interpreter])


if __name__ == '__main__':
    unittest.main()
