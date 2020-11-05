from person import Interpreter
from schedule import Schedule
from schedulers import Optimum
from consolereport import ConsoleReport
from csvprocessor import csv_to_list
from csvprocessor import create_appointment

# Variables
fh = 'DemoData.csv'
appts = []
appt_headers = ['Appt_ID', 'Start', 'Duration',
                'Appt_Priority', 'Appt_Prov', 'Appt_Interpreter']
patient_headers = ['Pat_ID', 'Pat_Name', 'Pat_Language', 'Pat_Gender']
location_headers = ['LocX', 'LocY', 'Building_Name', 'Clinic_Name']

# The exponential base with which appt are weighted (5**2, 5**3, ...)
BASE_WT = 5

# Areas
area1 = {'Building 1': BASE_WT, 'Building 2': 1, 'Building 3': 1,
         'Building 4': 1, 'Building 5': BASE_WT}
area2 = {'Building 1': 1, 'Building 2': BASE_WT, 'Building 3': 1,
         'Building 4': 1, 'Building 5': 1}
area3 = {'Building 1': 1, 'Building 2': 1, 'Building 3': BASE_WT,
         'Building 4': 1, 'Building 5': 1}
area4 = {'Building 1': 1, 'Building 2': 1, 'Building 3': 1,
         'Building 4': BASE_WT, 'Building 5': 1}
floater = {'Building 1': 1, 'Building 2': 1, 'Building 3': 1,
           'Building 4': 1, 'Building 5': 1}

# Interpreters
interp1 = Interpreter('Staff1', {'Spanish', 'Portuguese'},
                      'Female', '8:00', '16:30', area2)
interp2 = Interpreter('Staff1', {'Spanish', 'Portuguese'},
                      'Female', '10:30', '16:30', floater)
team = [interp1, interp2]

# Build headers
counter = 0
headers_dict = {}
rows = csv_to_list(fh)
for header in rows[0]:
    headers_dict[header] = counter
    counter += 1

# Build appointments list
for row_num in [key for key in rows.keys() if key > 0]:
    row = rows[row_num]
    appt = create_appointment(patient_headers, location_headers, appt_headers,
                              headers_dict, row)
    appts.append(appt)

sched = Schedule(appts, team)

# Compare scheduling method impact
opt = Optimum(sched)
report = ConsoleReport(opt)
report.print_comparison()
