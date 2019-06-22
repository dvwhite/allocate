import timeit
import datetime
import copy
from functools import wraps


def timer(method):
    """
    Method decorator to capture and print total run time in seconds
    :param method: The method or function to time
    :return: A function
    """
    @wraps(method)
    def wrapped(*args, **kw):
        timer_start = timeit.default_timer()
        result = method(*args, **kw)
        timer_finish = timeit.default_timer()
        print('%r  %2.2f s' % \
              (method.__name__, round((timer_finish - timer_start), 2)))
        return result
    return wrapped


def typedef(object_to_type):
    """
    An extension of the type function for custom class objects
    :param object_to_type: The object to type
    :return: A string
    """
    return type(object_to_type).__name__


def enumerate_combinations(iterable, length):
    """
    Enumerate all combinations of iterable elements of a given length
    :param iterable: An iterable, such as a list or tuple
    :param length: An integer specifying the length of the combination
    :return: A set
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in iterable:
                if item not in partial_sequence:
                    new_sequence = list(partial_sequence)
                    new_sequence.append(item)
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def sum_lists_product(list1, list2):
    """
    Return the sum of multiplying corresponding list elements
    :param list1: A list
    :param list2: A list
    :return: A number representing the sum
    """
    lst_sum = sum([x * y for x, y in zip(list1, list2)])
    return lst_sum


class Time(object):
    """
    A wrapper around the time library to encapsulate date/time arithmetic
    """
    def __init__(self, time, time_format):
        """
        Initialize the Time class
        :param time: A string representing the time, eg.: "08:00"
        :param time_format: The string format, eg.: "%H:%S"
        """
        self.format = time_format
        self.time = datetime.datetime.strptime(time, self.format)

    def copy(self):
        """
        Return a copy of self by value
        :return: A Time object
        """
        return copy.deepcopy(self)
    
    def change_to(self, time):
        """
        Change self.time to time
        :param time: A string representing the time, eg.: "O8:00"
        :return: None
        """
        self.time = datetime.datetime.strptime(time, self.format)
        
    def add_time(self, hours, minutes):
        """
        Add specified hour and minute quantities to self.time
        :param hours: A number of hours to add to self.time
        :param minutes: A number of minutes to add to self.time
        :return: None
        """
        self.time += datetime.timedelta(hours=hours, minutes=minutes)

    def time_difference(self, other):
        """
        Calculate hours, minutes difference between self.time and other time
        :param other: A Time object
        :return: A tuple
        """
        return (other.time.hour - self.time.hour,
                other.time.minute - self.time.minute)
    
    def __str__(self):
        try:
            dt = self.time
            time = f'{dt:%H}:{dt:%M}'
        except:
            time = self.time.strftime(self.format)
        return time

    def __eq__(self, other):
        if not isinstance(other, Time):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, Time):
            return True
        return self.__dict__ != other.__dict__

    def __le__(self, other):
        if not isinstance(other, Time):
            raise TypeError("'<=' not supported between instances of '" +
                            typedef(self) + "' and other types")
        return self.time <= other.time

    def __lt__(self, other):
        if not isinstance(other, Time):
            raise TypeError("'<' not supported between instances of '" +
                            typedef(self) + "' and other types")
        return self.time < other.time

    def __ge__(self, other):
        if not isinstance(other, Time):
            raise TypeError(
                "'>=' not supported between instances of '" +
                typedef(self) + "' and other types"
                )
        return self.time >= other.time

    def __gt__(self, other):
        if not isinstance(other, Time):
            raise TypeError(
                "'>' not supported between instances of '" +
                typedef(self) + "' and other types"
                )
        return self.time > other.time
