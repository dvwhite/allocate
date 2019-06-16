from person import Interpreter
from utils import Time
import unittest
import sys
sys.path.append('..')


class TestInterpreter(unittest.TestCase):
    """
    Tests the person.Interpreter class
    """
    def setUp(self):
        self.assignments = {}
        self.interpreter = Interpreter("Glott, Polly",
                                       ["English",
                                        "German",
                                        "Mandarin",
                                        "Japanese",
                                        "Spanish",
                                        "Russian"],
                                       "Female",
                                       "8:30",  "17:00",
                                       self.assignments)
        self.other = Interpreter("Smith, Jane",
                                 ["English"],
                                 "Female",
                                 "8:45",  "17:15",
                                 self.assignments)
        self.copied_interpreter = self.interpreter.copy()
        
    def test(self):
        interpreters = [self.other, self.interpreter]
        interpreters.sort()
        self.assertEqual(interpreters[0], self.interpreter)
        self.assertLess(self.interpreter, self.other)

        self.assertIsInstance(self.interpreter.shift_start, Time)
        self.assertIsInstance(self.interpreter.shift_finish, Time)
        self.assertIsInstance(self.copied_interpreter,  Interpreter)


if __name__ == '__main__':
    unittest.main()
