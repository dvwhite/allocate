import copy
import random
import collections
import sys
from location import (
    Grid,
    Point
)
from schedule import (
    Schedule,
    Appointment
)
from utils import (
    timer,
    Time,
    sum_lists_product,
    calc_arrival
)
from person import Patient
from constants import (
    TIME_FORMAT,
    WALKING_RATE
)


class ObjectInitializer(Grid):
    """
    Initializes scheduler objects
    """
    def __init__(self, schedule):
        """
        Initialize the ObjectInitializer class
        :param schedule: A Schedule object
        """
        Grid.__init__(self)
        self.schedule = schedule
        self.schedule_dict = {}
        self.appts_dict = {}
        self.appts_to_assign = list(schedule.appts)
        self.language_dict = collections.defaultdict(list)
        self.time_dict = collections.defaultdict(list)
        self.valid_choices = collections.defaultdict(list)
        self.patients = {appt.patient for appt in self.schedule.appts
                         if len(appt.patient) > 0}
        self.languages = set()
        self.jobs = {}
        self.schedule_paths = []
        self.best_paths = {}
        self.default_appt = Appointment(0, "00:00", 0,
                                        Patient(0, "None", [], "None"),
                                        Point(0, 0), 0, "", "").copy()
        self.interpreters = []
        self.init_all_objects()

    def init_job(self, interpreter, appt):
        """
        Add the interpreter's initial appointment to the job list
        :param interpreter: An Interpreter object
        :param appt: An Appointment object
        :return: None
        """
        if interpreter in self.jobs:
            raise ValueError('Interpreter exists in jobs.')
        self.jobs[interpreter] = [appt]

    def init_all_objects(self):
        """
        Wrapper for the two main initialization functions
        :return: None
        """
        self.populate_objects()
        self.populate_collections()        

    def populate_objects(self):
        """
        Processes self.schedule and builds objects used by other methods
        :return: None
        """
        # Reset interpreters to initial positions
        for interpreter in self.schedule.interpreters:
            if interpreter not in self.interpreters:
                self.interpreters.append(interpreter)

        for interpreter in self.interpreters:
            self.add_loc(interpreter, Point(0, 0))
            self.init_job(interpreter, self.default_appt)

        for patient in self.patients:
            for language in patient.languages:
                self.languages.add(language)
        self.default_appt.patient.languages = self.languages

        # Associate appts by idnum for optimization functions/objects
        for appt in self.schedule.appts:
            self.appts_dict[appt.idnum] = appt

    def populate_collections(self):
        """
        Processes self.schedule and builds collections used by other methods
        :return: None
        """
        self.gen_language_dict()

    def gen_language_dict(self):
        """
        Processes self.languages and builds a dict used by other methods
        :return: None
        """
        # This is a useful heuristic to reduce node size
        # processed by scheduling algorithms
        for language in self.languages:
            appts_in_lang = [appt for appt in self.appts_to_assign
                             if language in appt.patient.languages]
            self.language_dict[language] = appts_in_lang


class Reinitializer(ObjectInitializer):
    """
    Reinitialize objects initialized by ObjectInitializer
    """
    def __init__(self, schedule):
        """
        Initialize the Reinitializer class
        :param schedule: A Schedule object
        """
        ObjectInitializer.__init__(self, schedule)

    def reset(self):
        """
        Reinitialize the class
        :return: None
        """
        self._reset_attributes()
        self._reset_data_structures()
        self._reset_objects()

    def _reset_attributes(self):
        """
        Reinitialize class attributes
        :return: None
        """
        self.impact = 0
        self.schedule.impact = 0

    def _reset_data_structures(self):
        """
        Reinitialize class data structures
        :return: None
        """
        self.appts_to_assign = list(self.schedule.appts)
        self.time_dict = collections.defaultdict(list)
        self.valid_choices = collections.defaultdict(list)
        self.jobs = {}
        self.locs = {}
        self.schedule_dict = {}
        self.schedule_paths = []
        self.best_paths = {}

    def _reset_objects(self):
        """
        Reinitialize class objects
        :return: None
        """
        for appt in self.schedule.appts:
            appt.interpreter = ""
        for interpreter in self.interpreters:
            self.add_loc(interpreter, Point(0, 0))
            self.init_job(interpreter, self.default_appt)


class JobSupervisor(Reinitializer):
    """
    Keeps track of correctly assigning jobs to Interpreters
    """
    def __init__(self, schedule):
        """
        Initialize the JobSupervisor class
        :param schedule: A Schedule object
        """
        Reinitializer.__init__(self, schedule)
        self._populate_appts()

    def _populate_appts(self):
        """
        Add interpreter jobs for each job already in self.schedule.appts
        Should only be called by self.__init__
        :return: None
        """
        assigned_interpreters = [appt.interpreter for
                                 appt in self.schedule.appts if
                                 appt.interpreter]
        for interpreter in self.interpreters:
            if interpreter in assigned_interpreters:
                appts_assigned = [appt for appt in self.schedule.appts
                                  if appt.interpreter == interpreter]
                self.group_assign(interpreter, appts_assigned)

    def reset(self):
        """
        Reinitialize the class
        :return: None
        """
        super(JobSupervisor, self).reset()
        self._populate_appts()

    def get_job_with_id(self, job_id):
        """
        Get the appointment with the id number job_id
        :param job_id: An Appointment id number
        :return: An Appointment object
        """
        if job_id in self.appts_dict.keys():
            job = self.appts_dict[job_id]
            return job

    def get_jobs_with_ids(self, job_ids):
        """
        Get the appointments with the id numbers in ids
        :param job_ids: A list of Appointment id numbers
        :return: A list of Appointment objects
        """
        jobs_found = []
        for job_id in job_ids:
            job = self.get_job_with_id(job_id)
            if job:
                jobs_found.append(job)
        return jobs_found

    def get_last_job(self, interpreter):
        """
        Get the last job worked by interpreter
        :param interpreter: An interpreter object
        :return: An Appointment object
        """
        if interpreter not in self.jobs:
            raise ValueError('Interpreter not in jobs.')
        return self.jobs[interpreter][-1]

    def get_jobs(self, interpreter):
        """
        Get all jobs worked by interpreter
        :param interpreter: An Interpreter object
        :return: A list of Appointment objects
        """
        if interpreter not in self.jobs:
            raise ValueError('Interpreter not in jobs.')
        return self.jobs[interpreter]

    def add_job(self, interpreter, appt):
        """
        Add a new job to the jobs list for interpreter
        :param interpreter: An Interpreter object
        :param appt: An appointment object to add
        :return: None
        """
        if interpreter not in self.jobs:
            raise ValueError('Interpreter not in jobs.')
        jobs = self.jobs[interpreter]
        jobs.append(appt)
        jobs.sort()

    @staticmethod
    def calc_arrival(appt1, appt2):
        """
        Compute when staff would arrive at appt2 after finishing appt1
        :param appt1: An Appointment object (time order IS important)
        :param appt2: An Appointment object (time order IS important)
        :return: A Time object representing when staff could begin appt2
        """
        appts = [appt1, appt2]
        appts.sort()
        dist = int(appts[0].location.distance_from(appts[1].location))
        commute_time = round(dist / WALKING_RATE, 0)
        time = appts[0].finish.copy()
        time.add_time(hours=0, minutes=commute_time)
        time = max(time, appts[1].start.copy())
        return time

    def calc_impact(self):
        """
        Calculate the schedule's total impact score
        :return: A number representing the total impact score for self.schedule
        """
        return sum([appt.priority for appt in self.schedule.appts\
                    if len(appt.interpreter) > 0])

    @staticmethod
    def is_compatible_with_shift(interpreter, appt):
        """
        Check if appt intervals are compatible with the shift start and end times
        :param interpreter: An Interpreter object
        :param appt: An Appointment object
        :return: A Boolean indicating True if appt is compatible
        """
        if appt.start >= interpreter.shift_start and \
                appt.finish <= interpreter.shift_finish:
            return True
        return False

    def can_assign(self, interpreter, appt1, appt2=None):
        """
        Test if it's possible to assign both appt1 and appt2 to interpreter
        :param interpreter: An Interpreter object
        :param appt1: An Appointment object (order ISN'T important)
        :param appt2: An Appointment object (order ISN'T important)
        :return: A Boolean indicating that it can be assigned without overlap
        """
        if appt2 is None:
            appt2 = self.get_last_job(interpreter)
        appt_is_compatible = appt1.is_compatible(appt2)
        patient_is_compatible = (interpreter.is_compatible(appt1.patient) and
                                 interpreter.is_compatible(appt2.patient))
        shift_is_compatible = (self.is_compatible_with_shift(appt1) and
                               self.is_compatible_with_shift(appt2))
        return (appt_is_compatible and
                patient_is_compatible and
                shift_is_compatible)

    def can_insert_job(self, interpreter, appt):
        """
        Locate where to insert appointment and test for overlap with others
        :param interpreter: An Interpreter object
        :param appt: An Appointment object
        :return: A Boolean indicating that it can be inserted without overlap
        """
        try:
            interpreter_jobs = self.get_jobs(interpreter)
        except IndexError:
            interpreter_jobs = []
        if not interpreter_jobs:
            return True

        temp_lst = copy.deepcopy(interpreter_jobs)
        temp_lst.append(appt)
        temp_lst.sort()
        temp_index = temp_lst.index(appt)
        try:
            can_assign_before = self.can_assign(interpreter, appt,
                                                temp_lst[temp_index - 1])
        except IndexError:
            can_assign_before = True
        try:
            can_assign_after = self.can_assign(interpreter, appt,
                                               temp_lst[temp_index + 1])
        except IndexError:
            can_assign_after = True
        if can_assign_before and can_assign_after:
            return True
        return False

    def assign(self, interpreter, appt):
        """
        Assign the appointment to the Interpreter, adding it to his/her jobs
        :param interpreter: An Interpreter object
        :param appt: An Appointment object
        :return: None
        """
        if (not self.can_assign(interpreter, appt) or
                appt not in self.appts_to_assign):
            raise ValueError('Interpreter cannot be assigned to:'
                             + '\n' + str(appt) + ".")
        try:
            self.move_to(interpreter, appt.location)
        except ValueError:
            self.add_loc(interpreter, appt.location)
        try:
            self.add_job(interpreter, appt)
        except ValueError:
            self.init_job(interpreter, appt)
        appt.interpreter = interpreter
        if interpreter not in self.interpreters:
            self.interpreters.append(interpreter)
        self.appts_to_assign.remove(appt)
        self.schedule.impact += appt.priority

    def group_assign(self, interpreter, jobs):
        """
        Take a list of jobs and assign interpreter to each
        :param interpreter: An Interpreter object
        :param jobs: A list of Appointment objects
        :return: None
        """
        for job in jobs:
            self.assign(interpreter, job)


class AvailabilityCoordinator(JobSupervisor):
    """
    Coordinates the availability of Interpreter objects using Time dicts
    """
    def __init__(self, schedule):
        """
        Initialize the AvailabilityCoordinator class
        :param schedule: A Schedule object
        """
        JobSupervisor.__init__(self, schedule)
        
    def update_time_dict(self, time, appts):
        """
        A dict of Appointments in ascending order at or after a given time
        :param time: A Time object at or after which appts start
        :param appts: A collection of Appointment objects at or after time
        :return: None
        """
        self.time_dict = collections.defaultdict(list)
        for appt in appts:
            if appt.start >= time:
                appt_time = str(appt.start)
                self.time_dict[appt_time].append(appt)

    def rev_update_time_dict(self, time, appts):
        """
        A dict of Appointments in descending order at or after a given time
        :param time: A Time object at or before which appts start
        :param appts: A collection of Appointment objects at or before time
        :return: None
        """
        self.time_dict = collections.defaultdict(list)
        for appt in appts:
            if appt.start <= time:
                appt_time = str(appt.start)
                self.time_dict[appt_time].append(appt)

    def update_valid_choices(self, time, appts):
        """
        A dict of Appointment lists indexed to interpreters that can cover them
        Warning: Do not use if appointments are assigned out of sequence, or
        self.get_last_job(interpreter) will not work correctly
        :param time: A Time object to direct self.update_time_dict
        :param appts: A list of Appointment objects
        :return: None
        """
        self.update_time_dict(time, appts)
        self.valid_choices = collections.defaultdict(list)
        for interpreter in self.interpreters:
            time_when_available = self.get_last_job(interpreter).finish
            for appt_time, appt_list in self.time_dict.items():
                if Time(appt_time, TIME_FORMAT) >= time_when_available:
                    for appt in appt_list:
                        if self.can_assign(interpreter, appt):
                            self.valid_choices[interpreter].append(appt)

    def rev_update_valid_choices(self, time, appts):
        """
        A dict of Appointment lists indexed to interpreters that can cover them
        :param time: A Time object to direct self.rev_update_time_dict
        :param appts: A list of Appointment objects
        :return: None
        """
        self.rev_update_time_dict(time, appts)
        self.valid_choices = collections.defaultdict(list)
        for interpreter in self.interpreters:
            time_when_available = self.get_last_job(interpreter).finish
            for appt_time, appt_list in self.time_dict.items():
                if Time(appt_time, TIME_FORMAT) >= time_when_available:
                    for appt in appt_list:
                        if self.can_assign(interpreter, appt):
                            self.valid_choices[interpreter].append(appt)

    def next_valid_choice(self, interpreter, time, mode='after'):
        """
        Get next appointment that interpreter can do. It also has modes.
        :param interpreter: An Interpreter object
        :param time: A Time object
        :param mode: A string whether it should look after or before
        :return: An Appointment object
        """
        mode_dict = {'before': self.rev_update_valid_choices,
                     'after': self.update_valid_choices}
        mode_dict[mode](time, self.appts_to_assign)
        current_appt = self.get_last_job(interpreter)
        choices = self.valid_choices[interpreter]
        arrival_times = [self.calc_arrival(appt, current_appt)
                         for appt in choices]
        if len(choices) > 0:
            idx = arrival_times.index(min(arrival_times))
            return choices[idx]
        return None


class MonteCarlo(AvailabilityCoordinator):
    """
    Generate pseudo random schedules with variable impact scores
    """
    def __init__(self, schedule):
        """
        Initialize the MonteCarlo class
        :param schedule: A Schedule object
        """
        AvailabilityCoordinator.__init__(self, schedule)

    def optimized_random_schedule(self, time, printing=False):
        """
        Exhaust interpreter's availability by assigning randomly selected appts
        :param time: A Time object representing indicating minimum sᵢ
        :param printing: A Boolean whether to print status messages
        :return: A Schedule object
        """
        self.reset()
        for interpreter in self.interpreters:
            temp_lst = []
            for language in interpreter.languages:
                temp_lst += list(
                             [appt for appt in self.language_dict[language] if
                              appt in self.appts_to_assign and
                              appt.start >= time]
                             )
            while temp_lst:
                self.update_valid_choices(time, temp_lst)
                rand_appt = random.choice(temp_lst)
                is_valid_choice = self.can_insert_job(interpreter,
                                                      rand_appt)
                if is_valid_choice:
                    self.assign(interpreter, rand_appt)
                    if printing:
                        print(str(interpreter) +
                              " assigned to " +
                              str(rand_appt.idnum) +
                              ", priority = " +
                              str(rand_appt.priority))
                temp_lst.remove(rand_appt)
        return copy.deepcopy(self.schedule)

    @timer        
    def monte_carlo_trials(self, time, ntrials,
                           max_repeated=sys.maxsize, printing=False):
        """
        Assigns randomly selected appointments using Monte Carlo methods.
        It ends if the same value repeats a max num of consecutive trials.
        This is useful if you expect it to max out the value before ending.
        :param time: A Time object indicating minimum sᵢ
        :param ntrials: An integer number of Monte Carlo trials
        :param max_repeated = An integer number of Monte Carlo trials
        :param printing: A Boolean whether to print
        :return: A Schedule Object
        """
        best_schedule = None
        current_max = 0
        repeated = 0
        for idx in range(ntrials):
            self.reset()
            max_impact = current_max
            self.optimized_random_schedule(time, False)
            current_max = max(max_impact, self.schedule.impact)
            if current_max == max_impact:
                repeated += 1
            elif current_max > max_impact:
                best_schedule = copy.deepcopy(self.schedule)
                if printing:
                    print("New best found! trial#: " +
                          str(idx) + ", impact: " +
                          str(self.schedule.impact))
                repeated = 0
            if idx > 0 and idx % 10 == 0:
                if printing:
                    print("trial #" + str(idx) +
                          ", impact: " +
                          str(self.schedule.impact) +
                          ", Running best:" + str(current_max))
            if repeated >= max_repeated:
                break
        try:
            if printing:
                print("Best: " + str(best_schedule.impact))
        except:
            if printing:
                print("No best found.")
        return copy.deepcopy(best_schedule)


class Greedy(AvailabilityCoordinator):
    """
    Utilizes the greedy heuristic for scheduling optimization
    """
    def __init__(self, schedule):
        """
        Initialize the Greedy class
        :param schedule: A Schedule object
        """
        AvailabilityCoordinator.__init__(self, schedule)
        
    def select_highest_priority(self, interpreter, time, appts):
        """
        Return appointment in appts with the highest priority
        :param interpreter: An Interpreter object
        :param time: A Time object to direct self.update_valid_choices
        :param appts: A list of Appointment objects
        :return: An Appointment object
        """
        self.update_valid_choices(time, appts)
        current_max = 0
        highest_priority_appt = None
        try:
            interpreter_appts = self.valid_choices[interpreter]
        except:
            raise ValueError('Interpreter not in valid choices')
        for appt in interpreter_appts:
            max_value = current_max
            current_max = max(max_value, appt.priority)
            if current_max > max_value:
                highest_priority_appt = appt
        return highest_priority_appt       

    def process_args(self, optimal, appt_lst, interpreter):
        """
        Process args used to direct the Greedy methods of this class, which
        allows customization of the greedy strategy
        :param optimal: A string, 'weight' or 'number', to optimize for
        :param appt_lst: A list of Appointment objects
        :param interpreter: An Interpreter object
        :return: A tuple containing the optimal Appointment and a string
        """
        optimal = optimal.lower()
        if optimal == 'weight':
            # Scan wᵢ in the appt_list and select the maximum,
            # which is the highest priority
            priority_lst = list([(appt.priority, appt)
                                 for appt in appt_lst])
            highest_priority_appt = max(priority_lst)[1]
            greedy_appt = highest_priority_appt
            greedy_str = (str(interpreter) +
                          " assigned to " +
                          str(greedy_appt.idnum) +
                          ", priority = " +
                          str(greedy_appt.priority))
        elif optimal == 'number':
            # Scan fᵢ in the appt_lst and select the minimum,
            # which is the earliest finish time
            len_lst = list([(appt.finish, appt)
                            for appt in appt_lst])
            earliest_fi = min(len_lst)[1]
            greedy_appt = earliest_fi
            greedy_str = (str(interpreter) +
                          " assigned to " +
                          str(greedy_appt.idnum) +
                          ", finish = " +
                          str(greedy_appt.finish))
        else:
            raise ValueError('optimal is not a valid value.')
        return (greedy_appt, greedy_str)

    @timer
    def classic_greedy_schedule(self, time, optimal, printing=False):
        """
        Assigns appointments using a classic greedy strategy
        :param time: A Time object indicating minimum sᵢ
        :param optimal: A string, 'weight' or 'number', to optimize for
        :param printing: A Boolean whether or not to print status messages
        :return: A Schedule object
        """
        self.reset()
        greedy_appt = None
        is_valid_choice = False
        for interpreter in self.interpreters:
            appt_lst = []
            for language in interpreter.languages:
                appt_lst += list([appt for appt in
                                 self.language_dict[language]
                                 if (appt in self.appts_to_assign and
                                     appt.start >= time)])
            while appt_lst:
                self.update_valid_choices(time, appt_lst)
                greedy_appt, greedy_str = self.process_args(optimal,
                                                            appt_lst,
                                                            interpreter)
                if isinstance(greedy_appt, Appointment):
                    is_valid_choice = self.can_insert_job(interpreter,
                                                          greedy_appt)
  
                if is_valid_choice:
                    self.assign(interpreter, greedy_appt)
                    if printing: print(greedy_str)
                if greedy_appt in appt_lst:
                    appt_lst.remove(greedy_appt)
        return copy.deepcopy(self.schedule)

    @timer
    def balanced_greedy_schedule(self, time, optimal, printing=False):
        """
        Assigns appointments while balancing the load on each employee.
        :param time: A Time object indicating minimum sᵢ
        :param optimal: A string, 'weight' or 'number', to optimize for
        :param printing: A Boolean whether or not to print status messages
        :return: A Schedule object
        """
        self.reset()
        appts = {}
        for interpreter in self.interpreters:
            interpreter_list = []
            for language in interpreter.languages:
                for appt in self.language_dict[language]:
                    if appt in self.appts_to_assign and\
                       appt.start >= time:
                        interpreter_list.append(appt)
            appts[interpreter] = interpreter_list
            
        while appts:
            for interpreter in dict(appts):
                if len(appts[interpreter]) < 1:
                    del appts[interpreter]
                else:
                    appts_sublist = appts[interpreter]
                    self.update_valid_choices(time,
                                              appts_sublist)
                    greedy_data = self.process_args(optimal, appts_sublist,
                                                    interpreter)
                    greedy_appt, greedy_str = greedy_data
                    if isinstance(greedy_appt, Appointment):
                        is_valid_appt = self.can_insert_job(interpreter,
                                                                greedy_appt)
                    else:
                        is_valid_appt = False
                    if is_valid_appt:
                        self.assign(interpreter, greedy_appt)
                        if printing: print(greedy_str)
                        # Remove the assigned appointment from the other
                        # interpreters' appointment lists
                        appt_keys = set(appts.keys()) - {[interpreter]}
                        for interp_key in appt_keys:
                            if greedy_appt in appts[interp_key]:
                                appts[interp_key].remove(greedy_appt)
                    else:
                        appts[interpreter].remove(greedy_appt)
        return copy.deepcopy(self.schedule)

    @timer                        
    def group_greedy(self, interpreter_lists, optimal, balanced=False,
                     printing=False):
        """
        Greedy heuristic on each sublist in the interpreter_lists
        :param interpreter_lists:
        :param optimal: A string, 'weight' or 'number', to optimize for
        :param balanced: A Boolean whether to balance the load on employees
        :param printing: A Boolean whether or not to print status messages
        :return: A Schedule object
        """
        self.reset()
        current_interpreters = self.interpreters
        if printing: print(self.schedule.brief())
        for interpreter_sublist in interpreter_lists:
            if printing:
                print("Greedy for " +
                      str([interpreter.name for interpreter
                           in interpreter_sublist]) + "...")
            self.interpreters = interpreter_sublist
            if balanced:
                self.balanced_greedy_schedule(Time("00:00",  TIME_FORMAT),
                                              printing)
            else:
                self.classic_greedy_schedule(Time("00:00",  TIME_FORMAT),
                                             optimal, printing)
            if printing:
                print(self.schedule.brief())
        if printing:
            print("Impact: ", self.schedule.calc_impact())
        self.interpreters = current_interpreters
        sched_copy = self.schedule.copy()
        return sched_copy


class BruteForce(AvailabilityCoordinator):
    """
    Utilizes a brute force approach to computing as many of the
    total appointments in the power set as can reasonably be
    computed (given how many schedule order permutations you
    want to test) and selecting the list of valid, highest weight
    """
    def __init__(self, schedule):
        """
        Initialize the BruteForce class
        :param schedule:
        """
        AvailabilityCoordinator.__init__(self, schedule)

    def dfs_weighted(self, tree, start, finish, interpreter, lst):
        """
        DFS for max weight appointment list in the power set of appt lists
        :param tree: An adjacency list using idnums to represent node number
        :param start: The start time as a Time object
        :param finish: The finish time as a Time object
        :param interpreter: An Interpreter object
        :param lst: A list used for debugging, to be removed
        :return: A generator object
        """
        stack = [(start, [start])]
        appts_dict = self.appts_dict
        if interpreter not in self.best_paths:
            self.best_paths[interpreter] = (0, [])
        max_weight = self.best_paths[interpreter][0]
        while stack:
            (vertex, path) = stack.pop()
            for next in tree[vertex] - set(path):
                lst.append(path + [next])
                if next == finish:
                    weight = sum([appts_dict[ID].priority for ID in \
                                  (path + [next]) if ID in appts_dict])
                    if weight > max_weight:
                        self.best_paths[interpreter] = (weight, path + [next])
                        max_weight = weight
                    yield path + [next]
                else:
                    stack.append((next, path + [next]))

    def dfs_weighted_by_assignment(self, tree, start, finish, interpreter):
        """
        DFS for max weight appointment list in the power set of appt lists
        Weights used are modified beforehand by assignment multipliers
        :param tree: An adjacency list using idnums to represent node number
        :param start: The start time as a Time object
        :param finish: The finish time as a Time object
        :param interpreter: An Interpreter object
        :return: A generator object
        """
        stack = [(start, [start])]
        appts_dict = self.appts_dict
        if interpreter not in self.best_paths:
            self.best_paths[interpreter] = (0, [])
        max_weight = self.best_paths[interpreter][0]
        while stack:
            (vertex, path) = stack.pop()
            for next in tree[vertex] - set(path):
                if start < next:
                    break
                elif next == finish:
                    appt_wts = [appts_dict[ID].priority for ID in \
                                (path + [next]) if ID in appts_dict]
                    inter_wts = [interpreter.jobs[
                        appts_dict[ID].location.building
                        ] for ID in (path + [next]) if ID in appts_dict]
                    weight = sum_lists_product(appt_wts, inter_wts)
                    if weight > max_weight:
                        self.best_paths[interpreter] = (weight, path + [next])
                        max_weight = weight
                    yield path + [next]
                else:
                    stack.append((next, path + [next]))

    def gen_schedule_dict(self, interpreter, appts):
        """
        Modify self.schedule_dict to include appts that Interpreter can cover
        :param interpreter: An Interpreter object
        :param appts: A list of Appointment objects
        :return: None
        """
        self.schedule_dict = {}
        appts = copy.deepcopy(appts)
        sched = Schedule(appts, [interpreter])
        opt = Optimum(sched)
        opt.reset()
        opt_appts = opt.schedule.appts
        opt.update_valid_choices(interpreter.shift_start, opt_appts)
        temp_lst = [appt.idnum for appt in \
                    opt.valid_choices[interpreter]]
        temp_lst.sort()
        self.schedule_dict[0] = set(temp_lst)
        for appt in opt.valid_choices[interpreter]:
            opt.reset()
            opt.assign(interpreter, appt)
            appt.interpreter = ""
            opt.update_valid_choices(appt.finish, opt_appts)
            temp_lst = [appt.idnum for appt in \
                        opt.valid_choices[interpreter]]
            temp_lst.sort()
            self.schedule_dict[appt.idnum] = set(temp_lst)

    @timer
    def gen_all_paths(self, tree_function, interpreter):
        """
        The DFS core function that generates all paths through tree,
        it modifies self.schedule_paths or self.best_paths
        :param tree_function: An adjacency list (idnum: [idnums])
        :param interpreter: An Interpreter object
        :return: None
        """
        list_of_paths = []
        appts = list(self.appts_to_assign)
        appt_ids = [appt.idnum for appt in appts]
        sched = Schedule(appts, [interpreter])
        opt = Optimum(sched)
        opt.gen_schedule_dict(interpreter, appts)
        tree = dict(opt.schedule_dict)
        nodes = [node for node in tree if node > 0]  # skip the root
        for node in nodes:
            # This lets gen_all_paths iteratively explore the tree,
            # visiting only nodes that are processed instead of all possible
            node_idx = appt_ids.index(node)
            appts_subset = appts[:node_idx + 1]
            opt.gen_schedule_dict(interpreter, appts_subset)
            subtree = dict(opt.schedule_dict)
            # To guard against index errors, tamp down endNode
            (startNode, endNode) = (min(subtree),
                                    min(node, max(subtree)))
            list_of_paths.append(
                list(tree_function(subtree, startNode,
                                   endNode, interpreter))
                )
        self.schedule_paths = []
        for row in list_of_paths:
            for appt in row:
                self.schedule_paths.append(appt)
        if interpreter in opt.best_paths:
            self.best_paths[interpreter] = opt.best_paths[interpreter]

    @timer                        
    def group_gen_all_paths(self, tree_function, interpreters, printing=False):
        """
        Iteratively run tree_function on list of Interpreter objects
        :param tree_function: A function that iterates through the tree
        :param interpreters: A list of Interpreter objects
        :param printing: A Boolean whether to print status messages
        :return: A Schedule object
        """
        if printing: print(self.schedule.brief())
        for interpreter in interpreters:
            if printing:
                print("Finding optimal paths for " + str(interpreter) + "...")
            self.gen_all_paths(tree_function, interpreter)
            if interpreter in self.best_paths:
                appt_ids = [self.appts_dict[ID] for ID in
                            (self.best_paths[ interpreter][1])
                            if ID in self.appts_dict]
                jobs = self.get_jobs_with_ids(appt_ids)
                self.group_assign(interpreter, jobs)
        sched_copy = self.schedule.copy()
        return sched_copy

    def assign_optimal_schedule(self, printing=False):
        """
        Use dfs_weighted to generate the optimal schedule
        :param printing: A Boolean whether to print status messages
        :return: A Schedule object
        """
        self.reset()
        return self.group_gen_all_paths(self.dfs_weighted,
                                        self.interpreters, printing)
    
    def assign_optimal_job(self, printing=False):
        """
        Use dfs_weighted_by_assignment to generate the optimal schedule
        :param printing: A Boolean whether to print status messages
        :return: A Schedule object
        """
        self.reset()
        return self.group_gen_all_paths(self.dfs_weighted_by_assignment,
                                        self.interpreters, printing)

    @timer
    def debug_genpaths(self, interpreter):
        """
        Used to time how long it takes to process increasingly large path
        sizes. I use it to find the node where performance starts to suffer
        :param interpreter: An Interpreter object
        :return: None
        """
        self.reset()
        self.gen_schedule_dict(interpreter, self.appts_to_assign)
        for node in [node for node in self.schedule_dict.keys() if node > 1]:
            print("Calculating from nodes 1 to", node)
            self.test_node_paths(self.schedule_dict, 1, node, interpreter)

    @timer
    def test_node_paths(self, tree, start, finish, interpreter):
        """
        A debug script used to generate and print the optimal schedule
        :param tree: An adjacency list in form {idnum0: [idnum1, ...]}
        :param start: A Time object at or after which appts start
        :param finish: A Time object at or before which appts finish
        :param interpreter: An Interpreter object
        :return: A list
        """
        global lst1
        lst1 = []
        lst = list(self.dfs_weighted(tree, start, finish, interpreter, lst1))
        print("Finished:", len(lst), "paths generated")
        return lst1


class BruteForceDP(AvailabilityCoordinator):
    """
    Uses dynamic programming to reduce computational complexity of brute force
    """
    def __init__(self, schedule:Schedule):
        """
        Initialize the BruteForceDP class
        :param schedule: A schedule object
        """
        AvailabilityCoordinator.__init__(self, schedule)
        self.appt_weights = self.calculate_weights(self.appts_to_assign)

    @staticmethod
    def calculate_weights(appts):
        """
        Create a dictionary of appt weights used in compute_optimal
        Warning: Do not sort appts after running this function or
        you might lose track of the correct indices for each appt
        :param appts: a list of Interval objects
        :return: a dictionary of appt idnum: appt weight
        """
        weights = dict()
        weights[0] = 0
        for appt in appts[1:]:
            j = appts.index(appt)
            p = appt.get_prior_num(appts)
            weights[j] = max(appt.weight + weights[p],
                             weights[j-1])
        return weights

    def compute_optimal(self, j):
        """
        Recursively visits nodes in a list and selects the most highly
        weighted node at each edge, then proceeds from the optimal
        node to the next optimal node, repeating until j=0
        :param j: the idnum of the interval
        :return: A string
        """
        if j == 0:
            return 0
        else:
            appt = self.get_job_with_id(j)
            v = appt.priority
            p = appt.get_prior_num(self.appts_to_assign)
            if (v + self.appt_weights[p]) >= self.appt_weights[j-1]:
                return str(j) + ", " + str(self.compute_optimal(p))
            else:
                return self.compute_optimal(j-1)

    def schedule_str(self):
        """
        Returns the optimal appointment selections in a delimited string. I
        would suggest splitting it if you will do more than view it
        :return: A string
        """
        optimal_solution = self.compute_optimal(len(self.appts_to_assign) - 1)
        appt_lst = [int(idx) for idx in optimal_solution.split(sep=", ")]
        appt_lst.sort()
        print("")
        for idx in appt_lst[1:]:
            print(idx, self.appts_to_assign[idx])


class Optimum(BruteForce, Greedy, MonteCarlo):
    """
    Compares the performance of scheduling algorithms to display the optimum
    """
    def __init__(self, schedule):
        """
        Initialize the Optimum class
        :param schedule: A Schedule object
        """
        BruteForce.__init__(self, schedule)
        Greedy.__init__(self, schedule)
        MonteCarlo.__init__(self, schedule)
        self.default_time = Time("6:00", TIME_FORMAT)
        self.default_trials = 100
        self.max_repeated_result = max(self.default_trials // 4, 1)
        self.schedules = []
        self.has_compared = False
        self.schedule_methods = [self.classic_greedy_schedule,
                                 self.balanced_greedy_schedule,
                                 self.assign_optimal_schedule,
                                 self.assign_optimal_job]
      
    def call_method_default(self, method, printing=False):
        """
        Call method of some class using pre-defined (default) parameters
        :param method: The method to call
        :param printing: A Boolean whether to print status messages
        :return: Whatever the method called returns
        """
        optimal = 'weight'  # default
        args = {self.monte_carlo_trials: [self.default_time,
                                          self.default_trials,
                                          self.max_repeated_result, printing],
                self.classic_greedy_schedule: [self.default_time, optimal,
                                               printing],
                self.balanced_greedy_schedule: [self.default_time, optimal,
                                                printing],
                self.assign_optimal_schedule: [printing],
                self.assign_optimal_job: [printing]}
        if method in args.keys():
            lst = args[method]
            return method(*lst)
        else:
            return method()

    @timer
    def compare_performance(self, list_of_methods, printing=False):
        """
        Run each scheduling algoritm and compare the overall impact
        :param list_of_methods: Methods to run
        :param printing: A Boolean whether to print status messages
        :return: None
        """
        self.schedules = []
        for method in list_of_methods:
            method_name = method.__name__
            print('')
            print('Calling ' + method_name + '...')
            temp_sched = self.call_method_default(method, printing)
            score = temp_sched.calc_impact()
            self.schedules.append((score, method_name,
                                   copy.deepcopy(temp_sched)))
        self.has_compared = True
        
    def __hash__(self):
        return id(self)