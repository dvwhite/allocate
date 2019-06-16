from location import (
    Point,
    Grid
)
from person import Person
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Test the location.Grid class methods
    """
    def setUp(self):
        self.point = Point(1, 1)
        self.person = Person("Doe, Jane", ["English"], "Female")
        self.class_instance = Grid()
        
    def test(self):
        person = self.person
        point = self.point

        # add_loc method
        self.class_instance.add_loc(person, point)
        self.assertTrue(self.class_instance.locs[person], point)
        self.assertIsInstance(self.class_instance.locs[person], Point)

        # get_loc method
        self.assertTrue(self.class_instance.get_loc(person), point)
        self.assertIsInstance(self.class_instance.get_loc(person), Point)

        # move_to method
        new_point = Point(0, 0)
        self.class_instance.move_to(person, new_point)
        self.assertIsInstance(self.class_instance.locs[person], Point)
        self.assertEquals(self.class_instance.get_loc(person).x, 0)
        self.assertEquals(self.class_instance.get_loc(person).y, 0)


if __name__ == '__main__':
    unittest.main()
