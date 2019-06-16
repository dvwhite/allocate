from utils import Time
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    def setUp(self):
        self.time = Time("08:00",  "%H:%M")
        
    def test(self):
        # copy method
        new_instance = self.time.copy()
        self.assertIsInstance(new_instance,  Time)
        self.assertEqual(new_instance,  self.time)
        
        # change_to method
        new_time = "08:01"
        new_instance.change_to(new_time)
        self.assertEqual(str(new_instance),  new_time)
        
        # add_time method
        new_instance.add_time(1,  1)
        self.assertEqual(str(new_instance),  "09:02")
        new_instance.add_time(-10,  -3)
        self.assertEqual(str(new_instance),  "22:59")
        
        # time_difference method
        hours,  minutes = self.time.time_difference(new_instance)
        self.assertEqual((hours,  minutes),  (14,  59))
        
        # str method
        self.assertEqual(str(self.time),  "08:00")


if __name__ == '__main__':
    unittest.main()
