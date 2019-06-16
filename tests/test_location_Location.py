from location import Location
import unittest
import sys
sys.path.append('..')


class TestClass(unittest.TestCase):
    """
    Tests location.Location class
    """
    def setUp(self):
        self.loc = Location(1,  1,  "Hospital",  "Clinic")
        
    def test(self):
        # properties
        self.assertTrue(self.loc.building,  "Hospital")
        self.assertTrue(self.loc.clinic,  "Clinic")
        # str method
        self.assertTrue(str((self.loc.building,  self.loc.clinic)),
                        str(self.loc))


if __name__ == '__main__':
    unittest.main()
