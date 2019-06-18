from schedulers import JobSupervisor
from location import Point
from tests.objects import (
    test_schedule,
    appt4,
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
        self.job_supervisor = JobSupervisor(self.schedule)
        
    def test(self):
        appts = self.job_supervisor.schedule.appts
        interpreters = self.job_supervisor.interpreters

        # get_job_with_id
        # Returns an appointment from self.appt_dict at index id
        # Due to overlap with the id builtin, the variable name is job_id
        #
        # This test indexes a pre-made test object and assert
        # equality to the index as the first test condition
        # If this test fails then the test object has been changed
        self.assertEqual(appts[0].idnum, 1)
        self.assertEqual(self.job_supervisor.get_job_with_id(1), appts[0])

        # get_jobs_with_ids
        # Calls get_job_with_id on each id and returns a list of appts found
        # Asserting object equality by index ensures no mutation interference
        ids1 = [1, 2, 3]
        ids2 = [1, 2, 7]
        ids3 = [5, 6, 7]
        self.assertEqual(appts[0].idnum, ids1[0])
        self.assertEqual(appts[1].idnum, ids1[1])
        self.assertEqual(appts[2].idnum, ids1[2])
        test_list = self.job_supervisor.get_jobs_with_ids(ids1)
        self.assertEqual([appts[0], appts[1], appts[2]], test_list)

        self.assertEqual(appts[0].idnum, ids1[0])
        self.assertEqual(appts[1].idnum, ids1[1])
        test_list = self.job_supervisor.get_jobs_with_ids(ids2)
        self.assertEqual([appts[0], appts[1]], test_list)

        test_list = self.job_supervisor.get_jobs_with_ids(ids3)
        self.assertEqual([], test_list)

        # get_last_job
        job = self.job_supervisor.get_last_job(interpreters[0])
        self.assertEqual(job, appts[0])

        job = self.job_supervisor.get_last_job(interpreters[1])
        self.assertEqual(job, appts[1])

        job = self.job_supervisor.get_last_job(interpreters[2])
        self.assertEqual(job, appts[2])

        # get_jobs
        jobs = self.job_supervisor.get_jobs(interpreters[0])
        self.assertEqual(jobs, [self.job_supervisor.default_appt,
                                appts[0]])

        jobs = self.job_supervisor.get_jobs(interpreters[1])
        self.assertEqual(jobs, [self.job_supervisor.default_appt,
                                appts[1]])

        jobs = self.job_supervisor.get_jobs(interpreters[2])
        self.assertEqual(jobs, [self.job_supervisor.default_appt,
                                appts[2]])

        # add_job
        self.job_supervisor.add_job(interpreters[2], appt4)
        jobs = self.job_supervisor.get_jobs(interpreters[2])
        self.assertEqual(jobs, [self.job_supervisor.default_appt,
                                appts[2],
                                appt4])

        # calc_impact
        self.assertEqual(self.job_supervisor.calc_impact(), 150)

        # can_assign
        self.assertTrue(self.job_supervisor.can_assign(interpreters[0],
                                                       appts[0],
                                                       appts[1]))
        self.assertFalse(self.job_supervisor.can_assign(interpreters[0],
                                                        appts[0],
                                                        appts[0]))

        # can_insert_job
        self.job_supervisor.appts_to_assign.append(appt6)
        self.assertTrue(self.job_supervisor.can_insert_job(interpreters[0],
                                                           appt6))
        self.job_supervisor.assign(interpreters[0], appt6)
        self.assertFalse(self.job_supervisor.can_insert_job(interpreters[0],
                                                            appt7))

        # assign
        # save existing assigned staff before reset
        interpreter = appts[0].interpreter
        # reset objects
        appts[0].interpreter = ""
        self.job_supervisor.jobs[interpreter].remove(appts[0])
        self.job_supervisor.move_to(interpreter, Point(0, 0))
        self.job_supervisor.appts_to_assign.append(appts[0])

        # assign the interpreter to the appointment
        self.job_supervisor.assign(interpreter, appts[0])
        self.assertEqual(appts[0].interpreter, interpreter)
        self.assertIn(appts[0], self.job_supervisor.jobs[interpreter])
        self.assertEqual(Point(*appts[0].location.coordinates),
                         self.job_supervisor.locs[interpreter])

        # group_assign
        # reset appts[0]
        self.job_supervisor.jobs[interpreter].remove(appts[0])
        self.job_supervisor.move_to(interpreter, Point(0, 0))
        self.job_supervisor.appts_to_assign.append(appts[0])
        # reset appt6
        self.job_supervisor.jobs[interpreter].remove(appt6)
        self.job_supervisor.move_to(interpreter, Point(0, 0))
        self.job_supervisor.appts_to_assign.append(appt6)

        # create jobs and call the method under test
        jobs = [appts[0], appt6]
        self.job_supervisor.group_assign(interpreter, jobs)
        # check for appts[0] assignment
        self.assertEqual(appts[0].interpreter, interpreter)
        self.assertIn(appts[0], self.job_supervisor.jobs[interpreter])
        # check for appt6 assignment
        self.assertEqual(appt6.interpreter, interpreter)
        self.assertIn(appt6, self.job_supervisor.jobs[interpreter])


if __name__ == '__main__':
    unittest.main()
