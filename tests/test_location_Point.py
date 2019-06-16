from location import Point
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    def setUp(self):
        self.obj = Point(10,  0)
        
    def test(self):
        # attributes
        test_point = (10,  0)
        self.assertEqual(10,  self.obj.x)
        self.assertEqual(0,  self.obj.y)
        self.assertEqual(test_point,  self.obj.coordinates)

        # move method
        point2 = Point(10,  10)
        point2 = point2.move(1, 1)
        self.assertEqual(Point(11,  11), point2)

        # move_to method
        point3 = Point(1,  1)
        point3 = point3.move_to(point2.x,  point2.y)
        self.assertEqual(point2,  point3)

        # distance_from method
        point1 = Point(1,  1)
        point2 = Point(4,  5)
        dist = point1.distance_from(point2)
        self.assertEqual(5,  dist)

        # str method
        string_repr = str(point2)
        self.assertEqual(str((4,  5)),  string_repr)


if __name__ == '__main__':
    unittest.main()
