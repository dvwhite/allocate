from person import Patient
import unittest
import sys
sys.path.append('..')


class TestPatient(unittest.TestCase):
    def setUp(self):
        self.patient = Patient(1,  "Doe, John",
                               ["English",  "German"],  "Male")
        
    def test(self):
        self.assertTrue(self.patient.idnum,  1)
        self.assertIsInstance(self.patient.copy(),  Patient)


if __name__ == '__main__':
    unittest.main()
