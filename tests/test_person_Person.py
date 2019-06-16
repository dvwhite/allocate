from person import Person
import unittest
import sys
sys.path.append('..')


class TestPerson(unittest.TestCase):
    """
    Tests the person.Person class
    """
    def setUp(self):
        self.person = Person("Doe, John",  {"English",  "German"},  "Male")
        
    def test(self):
        # speaks method
        self.assertTrue(self.person.speaks(list(self.person.languages)[0]))
        self.assertTrue(self.person.speaks(list(self.person.languages)[1]))
        self.assertFalse(self.person.speaks('Swahili'))
        self.assertFalse(self.person.speaks(''))
        # has_common_language method
        person2 = Person("Suzuki, Joe",  {"Japanese", "Korean"},  "Male")
        self.assertTrue(self.person.has_common_language(self.person))
        self.assertFalse(self.person.has_common_language(person2))
        # copy method
        new_person = self.person.copy()
        self.assertIsInstance(new_person,  Person)
        self.assertTrue(new_person == self.person)


if __name__ == '__main__':
    unittest.main()
