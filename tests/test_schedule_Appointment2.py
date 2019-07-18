from schedule import (
    Appointment,
    Schedule
)
from person import (
    Patient,
    Interpreter
)
from location import Location
from schedulers import BruteForceDP as bfd
from utils import Time
from constants import TIME_FORMAT
from operator import attrgetter
import unittest
import sys
sys.path.append('..')


class TestSomething(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        pat1 = Patient(1, 'One', {'Spanish'}, 'Male')
        pat2 = Patient(2, 'Two', {'Spanish'}, 'Male')
        pat3 = Patient(3, 'Three', {'Spanish'}, 'Male')
        pat4 = Patient(4, 'Four', {'Spanish'}, 'Male')
        pat5 = Patient(5, 'Five', {'Spanish'}, 'Male')
        loc1 = Location(0, 0, "Building", "Clinic")
        a1 = Appointment(1, "8:00", 15, pat1, loc1, 1, "Dr.", "")
        a2 = Appointment(2, "8:10", 30, pat2, loc1, 2, "Dr.", "")
        a3 = Appointment(3, "8:30", 20, pat1, loc1, 3, "Dr.", "")
        a4 = Appointment(4, "8:45", 35, pat2, loc1, 4, "Dr.", "")
        a5 = Appointment(5, "9:30", 35, pat2, loc1, 5, "Dr.", "")
        a6 = Appointment(6, "9:00", 75, pat3, loc1, 6, "Dr.", "")
        a7 = Appointment(7, "8:35", 150, pat4, loc1, 7, "Dr.", "")
        a8 = Appointment(8, "8:30", 180, pat5, loc1, 8, "Dr.", "")
        appts = [a1, a2, a3, a4, a5, a6, a7, a8]
        sched = Schedule(appts,
                         [Interpreter("Inter",
                                      {'Spanish', 'English'},
                                      "Male",
                                      "8:00",
                                      "17:00",
                                      {}
                                      )
                          ]
                         )
        inter = sched.interpreters[0]
        precalculated_p = {1: 0, 2: 0, 3: 1, 4: 2, 5: 4, 6: 3, 7: 1, 8: 1}
        precalculated_weights = {1: 1, 2: 2, 3: 4, 4: 6, 5: 11, 6: 11,
                                 7: 11, 8: 11}

        cls = bfd(sched)
        p_dict = {}
        for appt in appts:
            prior = appt.calc_prior2(appts)
            if prior is not None:
                p_dict[appt.idnum] = prior.idnum
            else:
                p_dict[appt.idnum] = 0
        # This tests whether calc_prior returns the correct indices
        self.assertEqual(p_dict, precalculated_p)




if __name__ == '__main__':
    unittest.main()
