from operator import attrgetter
from utils import (
    typedef,
    Time,
    calc_arrival
)
from constants import TIME_FORMAT
import bisect
import copy


class Appointment(object):
    """
    An encounter with fixed start and end times, and one patient
    """
    def __init__(self, idnum, start, duration_in_mins, patient, location,
                 priority, provider, interpreter):
        """
        Initialize the Appointment class
        :param idnum: An integer representing the appointment id number
        :param start: A Time object of the appointment start time
        :param duration_in_mins: The minutes from appointment start to finish
        :param patient: A string representing patient name
        :param location: A string representing the title of the location
        :param priority: A number for the appointment weight
        :param provider: A string representing the provider name
        :param interpreter: A string representing the interpreter name
        """
        self.idnum = idnum
        self.start = Time(start, TIME_FORMAT)
        self.duration = duration_in_mins
        self.finish = Time(start, TIME_FORMAT)
        self.finish.add_time(hours=0, minutes=duration_in_mins)
        self.patient = patient
        self.location = location
        self.priority = priority
        self.provider = provider
        self.interpreter = interpreter
        self.late_allowed = 0

    def brief(self):
        """
        Returns a briefer representation of class methods than __str__
        :return: String
        """
        temp_str = ""
        separator_char = "|"
        properties_lst = [self.idnum, self.start, self.finish, self.patient,
                          self.location.coordinates, self.interpreter]
        num_iterated = 0
        for val in properties_lst:
            if len(temp_str) < 1:
                temp_str = str(val)
            else:
                temp_str += str(val)
            if num_iterated < (len(properties_lst) - 1):
                temp_str += separator_char
            num_iterated += 1
        return temp_str

    def copy(self):
        return copy.deepcopy(self)

    def distance_from(self, other):
        """
        Distance from another Appointment using Pythagorean distance formula
        :param other: Another Interval object compared to self
        :return: A float representing distance
        """
        dist = self.location.distance_from(other.location)
        return dist

    def is_compatible(self, other):
        """
        Test whether self and other are not overlapping appointments
        :param other: An Appointment object
        :return: Boolean indicating if they're compatible
        """
        appts = [self, other]
        appts.sort(key=attrgetter('start'), reverse=False)
        first_appt = appts[0]
        second_appt = appts[1]
        arrival_time = calc_arrival(first_appt, second_appt)
        second_time = second_appt.start.copy()
        second_time.add_time(hours=0, minutes=self.late_allowed)
        return arrival_time <= second_time

    def calc_prior(self, others):
        """
        Returns the idnum of the rightmost compatible interval
        :param others: a list of Interval objects
        :return: An Interval object
        """
        others_copy = copy.deepcopy(others)
        others_copy.sort(reverse=False)
        self_idx = others.index(self)
        start = [interval.start for interval in others_copy]
        finish = [interval.finish for interval in others_copy]
        rightmost = bisect.bisect_right(finish, start[self_idx])
        others_rightmost = others_copy[:rightmost]
        compatible_idx = [others.index(other) for other in others_rightmost]
        compatible_idx.sort(reverse=True)
        for idx in compatible_idx:
            other = others[idx]
            if other.is_compatible(self):
                return other

    def calc_prior2(self, others):
        lst = copy.deepcopy(others)
        lst.sort(key=attrgetter('finish'), reverse=False)
        finish = [other.finish for other in others]
        pos = bisect.bisect(finish, self.finish)
        valid_others = [other for other in others[:pos] if
                        other.finish <= self.start]
        if valid_others:
            return valid_others[-1]

    def get_prior_num(self, others):
        """
        Handle output of calc_prior, coercing None to 0
        :param others: a list of Interval objects
        :return: An integer idnum
        """
        prior = self.calc_prior2(others)
        if prior is None:
            prior_num = 0
        else:
            # prior_num = others.index(prior)
            prior_num = prior.idnum
        return prior_num

    def __str__(self):
        temp_str = ""
        delimiter = "|"
        num_keys_iterated = 0
        attributes = self.__dict__
        for key, val in attributes.items():
            if len(temp_str) < 1:
                temp_str = str(val)
            else:
                temp_str += str(val)
            if num_keys_iterated < (len(attributes) - 1):
                temp_str += delimiter
            num_keys_iterated += 1
        return temp_str

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if not isinstance(other, Appointment):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, Appointment):
            return True
        return self.__dict__ != other.__dict__

    def __lt__(self, other):
        """
         Facilitate sorting by start times by comparing Time objects
         :param other: Another Interval object
         :return: Boolean indicating comparison result
        """
        if not isinstance(other, Appointment):
            raise TypeError("'<' not supported between instances of '" +
                            typedef(self) + "' and other types")
        
        return self.start < other.start


class Schedule(object):
    """
    Collection of weighted Appointment objects
    """
    def __init__(self, appts, interpreters):
        """
        Initialize the Schedule class, sort .appts, calculate .total_impact
        :param appts: A list of Appointment objects
        :param interpreters: A list of Interpreter objects
        """
        self.appts = list(appts)
        self.appts.sort()
        self.interpreters = interpreters
        self.impact = 0
        self.total_impact = sum([appt.priority for appt in self.appts])

    def calc_impact(self):
        """
        Sum the impact for each Appointment in self.appts
        :return: A numeric sum value
        """
        return sum([appt.priority for appt in
                    self.appts if len(appt.interpreter) > 0])

    def copy(self):
        return copy.deepcopy(self)

    def gen_intervals(self):
        """
        Generate a dictionary of interval property lists used in the weighted
        interval scheduling algorithm
        :return: A dictionary of string:list
        """
        idx = []
        start = []
        finish = []
        weight = []
        x_coord = []
        y_coord = []
        for appt in self.appts:
            idx.append(appt.idnum)
            start.append(str(appt.start))
            finish.append(str(appt.finish))
            weight.append(appt.priority)
            x_coord.append(appt.location.x)
            y_coord.append(appt.location.y)
        intervals = {"i": idx,
                     "s": start,
                     "f": finish,
                     "v": weight,
                     "x": x_coord,
                     "y": y_coord}
        return intervals

    def brief(self):
        """
        Returns a briefer representation of class methods than __str__
        :return: A string
        """
        appt_str = ""
        for appt in self.appts:
            if len(appt_str) < 1:
                appt_str = appt.brief() + "\n"
            else:
                appt_str += appt.brief() + "\n"
        return appt_str

    def __str__(self):
        appt_str = ""
        for appt in self.appts:
            if len(appt_str) < 1:
                appt_str = str(appt) + "\n"
            else:
                appt_str += str(appt) + "\n"
        return appt_str

    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, Schedule):
            return True
        return self.__dict__ != other.__dict__
