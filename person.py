from utils import (
    Time,
    typedef
)
from constants import TIME_FORMAT
import copy


class Person(object):
    """
    A base class for all people
    """

    def __init__(self, name, languages, gender):
        """
        Initialize the Person object
        :param name: A string representing the name
        :param languages: A set of strings, the languages spoken by Person
        :param gender: A string representing the person's gender
        """
        self.name = name
        self.languages = languages
        self.gender = gender

    def speaks(self, language):
        """
        Test if person can speak language
        :param language: A string representing a language
        :return: A Boolean indicating if self speaks language
        """
        return language in self.languages

    def has_common_language(self, other):
        """
        Test if self has at least one language in common with other
        :param other: A Person (or inherited object)
        :return: A Boolean indicating mutual intelligibility
        """
        return self.languages & other.languages

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return self.name

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return id(self)


class Patient(Person):
    """
    A person with the addition of a patient id number
    """

    def __init__(self, idnum, name, languages, gender):
        Person.__init__(self, name, languages, gender)
        self.idnum = idnum


class Interpreter(Person):
    """
    A person working a shift with start and finish times, and assignments
    """

    def __init__(self, name, languages, gender, shift_start, shift_finish,
                 assignments):
        """
        Initialize the Interpreter class
        :param name: A string
        :param languages: A list of strings representing languages spoken
        :param gender: A string
        :param shift_start: A string for the start time, eg.: "08:00"
        :param shift_finish: A string for the finish time, eg.: "17:00"
        :param assignments: A dictionary mapping building names to weights
        """
        Person.__init__(self, name, languages, gender)
        self.shift_start = Time(shift_start, TIME_FORMAT)
        self.shift_finish = Time(shift_finish, TIME_FORMAT)
        self.assignments = assignments

    def is_compatible(self, other):
        """
        Test if self can be assigned to other. Currently, the criterion is
        mutual intelligibility (has_common_language) but can be expanded
        :param other: Another Person or subclass of Person
        :return: A Boolean whether self can be assigned to other
        """
        return self.has_common_language(other)

    def __lt__(self, other):
        """
        Override default method when sorting lists of self by start time
        :param other: An Interpreter object
        :return: A Boolean indicating if self.start is before other.start
        """
        if not isinstance(other, Interpreter):
            raise TypeError("'<' not supported between instances of '" +
                            typedef(self) + "' and other types")
        return self.shift_start < other.shift_start
