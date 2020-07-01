from schedulers import Optimum
from location import Point


class ConsoleReport(Optimum):
    """
    Write a text-based report to the console that
    ranks the scheduling methods by total score
    """
    def __init__(self, optimum):
        Optimum.__init__(self, optimum.schedule)
        self.schedules = optimum.schedules
        self.has_compared = optimum.has_compared

    def print_comparison(self):
        scores_exist = self.has_compared
        if scores_exist:
            self.generate_text()

    def generate_text(self):
        if len(self.schedules) > 0:
            max_impact = self.schedule.total_impact
            print('')
            print('Performance Comparison of Scheduling Methods')
            print('--------------------------------------------')
            print('')
            print('Impact score at 100% staffing:', str(max_impact))
            print('')
            print('Method scores (in descending order):')
            self.schedules.sort(reverse=True)
            for (score, methodName, sched) in self.schedules:
                score_percent = round(score / max_impact * 100, 2)
                print('   ' + methodName +
                      ', Score: ' + str(score) +
                      ' (' + str(score_percent) + '%)')
            print('')
            for (score, methodName, sched) in self.schedules:
                input('Press enter to continue...\n')
                print(methodName + ' assignments:')
                # temp_opt = Optimum(sched)
                # temp_opt.print_all_assignments()
                self.schedule = sched
                self.interpreters = sched.interpreters
                self.print_all_assignments()

            inp = input('Press enter to close...')
            print(inp)

    def print_valid_choices(self, interpreters):
        """
        Print the valid appointment choices for self.interpreters
        """
        for interpreter in interpreters:
            print('\n' + str(interpreter))
            try:
                int_appt = self.get_last_job(interpreter)
                int_location = int_appt.location
                print("Current: " + str(int_appt.start) + " - " +
                      str(int_appt.finish) + ", at location " +
                      str(int_appt.location.coords) + '\n')
            except:
                int_location = Point(0, 0)
                print(
                    "Not currently assigned to an appointment." + '\n'
                    )
            for appt in self.valid_choices[interpreter]:
                    print('\t' + str(appt.IDNum) + " " +
                          str(appt.start) +
                          " - " +
                          str(appt.finish) + " " +
                          str((appt.location.x, appt.location.y)) +
                          " " +
                          str(round(
                              appt.location.distanceFrom(int_location)))
                          )

    def print_assignments(self, interpreter):
        """
        Print the appointments assigned to interpreter
        """
        if len(interpreter) > 0:
            msg = ('Appointments assigned to ' + str(interpreter) + ':\n' +
                   'Available ' + str(interpreter.shift_start) +
                   "-" + str(interpreter.shift_finish))
        else:
            msg = 'Appointments not assigned:'
        try:
            appts_to_print = [appt for appt in self.schedule.appts
                              if appt.interpreter == interpreter]
        except:
            if len(interpreter) < 1:
                appts_to_print = [appt for appt in self.schedule.appts
                                  if len(appt.interpreter) < 1]
            else:
                appts_to_print = ["None"]
        impact = sum([appt.priority for appt in appts_to_print])
        num_appts = len(appts_to_print)
        
        print(msg)
        print('Impact:' + str(impact))
        print('Number:' + str(num_appts))
        print('')

        for appt in appts_to_print:
            print(appt)
        print('\n')

    def print_all_assignments(self):
        """
        Print the appointments assigned to self.interpreters
        """
        interpreters = list(self.interpreters) + ['']
        for interpreter in interpreters:
            self.print_assignments(interpreter)
