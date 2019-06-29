from schedule import (
    Schedule,
    Appointment
)
from person import (
    Patient,
    Interpreter
)
from location import Location
import sys
sys.path.append('..')

general_rotation = {"Central Hospital": 1, "West Wing": 1, "East Wing": 1}

patient1 = Patient(idnum=1,
                   name="Joe Spanish",
                   languages={"Spanish"},
                   gender="Male")

patient2 = Patient(idnum=2,
                   name="John French",
                   languages={"French"},
                   gender="Male")

interpreter1 = Interpreter(name="Jose Gomez",
                           languages={"Spanish", "English"},
                           gender="Male",
                           shift_start="8:00",
                           shift_finish="16:30",
                           assignments=general_rotation)

interpreter2 = Interpreter(name="Janet Gomez",
                           languages={"Spanish", "English"},
                           gender="Female",
                           shift_start="8:00",
                           shift_finish="17:00",
                           assignments=general_rotation)

interpreter3 = Interpreter(name="Francois Thames",
                           languages={"French", "English"},
                           gender="Male",
                           shift_start="8:30",
                           shift_finish="12:30",
                           assignments=general_rotation)

# 0, 0
loc1 = Location(x=0,
                y=0,
                building="Central Hospital",
                clinic="Radiology")

# 4, 4
loc2 = Location(x=0,
                y=0,
                building="West Wing",
                clinic="Ophthalmology")

# 3, 4
loc3 = Location(x=0,
                y=0,
                building="East Wing",
                clinic="Emergency Room")

# 0, -1
loc4 = Location(x=0,
                y=0,
                building="Central Hospital",
                clinic="GI Clinic")

# -2, -2
loc5 = Location(x=0,
                y=0,
                building="East Wing",
                clinic="General Med")

# -1, 2
loc6 = Location(x=0,
                y=0,
                building="Central Hospital",
                clinic="Pulmonary Clinic")

# -5, -3
loc7 = Location(x=0,
                y=0,
                building="West Wing",
                clinic="General Surgery Clinic")

appt1 = Appointment(idnum=1,
                    start="8:00",
                    duration_in_mins=10,
                    patient=patient1,
                    location=loc3,
                    priority=100,
                    provider="Dr. John",
                    interpreter=interpreter1)

appt2 = Appointment(idnum=2,
                    start="8:25",
                    duration_in_mins=40,
                    patient=patient1,
                    location=loc1,
                    priority=30,
                    provider="Dr. Jake",
                    interpreter=interpreter2)

appt3 = Appointment(idnum=3,
                    start="8:45",
                    duration_in_mins=40,
                    patient=patient2,
                    location=loc2,
                    priority=20,
                    provider="Dr. Jane",
                    interpreter=interpreter3)

appt4 = Appointment(idnum=4,
                    start="9:45",
                    duration_in_mins=40,
                    patient=patient2,
                    location=loc2,
                    priority=20,
                    provider="Dr. Jane",
                    interpreter="")

appt5 = Appointment(idnum=5,
                    start="12:45",
                    duration_in_mins=40,
                    patient=patient2,
                    location=loc2,
                    priority=20,
                    provider="Dr. Jane",
                    interpreter="")


appt6 = Appointment(idnum=6,
                    start="13:45",
                    duration_in_mins=90,
                    patient=patient1,
                    location=loc2,
                    priority=20,
                    provider="Dr. Jane",
                    interpreter="")

appt7 = Appointment(idnum=7,
                    start="14:05",
                    duration_in_mins=30,
                    patient=patient1,
                    location=loc2,
                    priority=20,
                    provider="Dr. Jane",
                    interpreter="")

appt8 = Appointment(idnum=1, start='08:00', duration_in_mins=75,
                    patient=patient1, location=loc4, priority=85,
                    provider="Dr. Jane", interpreter='')
appt9 = Appointment(idnum=2, start="08:00", duration_in_mins=55,
                    patient=patient1, location=loc5, priority=215,
                    provider="Dr. Jane", interpreter='')
appt10 = Appointment(idnum=3, start="08:00", duration_in_mins=375,
                     patient=patient1, location=loc6, priority=85,
                     provider="Dr. Jane", interpreter='')
appt11 = Appointment(idnum=4, start="08:15", duration_in_mins=60,
                     patient=patient1, location=loc6, priority=213,
                     provider="Dr. Jane", interpreter='')
appt12 = Appointment(idnum=5, start="08:30", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt13 = Appointment(idnum=6, start="08:30", duration_in_mins=30,
                     patient=patient1, location=loc7, priority=115,
                     provider="Dr. Jane", interpreter='')
appt14 = Appointment(idnum=7, start="09:00", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt15 = Appointment(idnum=8, start="09:00", duration_in_mins=35,
                     patient=patient1, location=loc5, priority=115,
                     provider="Dr. Jane", interpreter='')
appt16 = Appointment(idnum=9, start="09:00", duration_in_mins=75,
                     patient=patient1, location=loc6, priority=212,
                     provider="Dr. Jane", interpreter='')
appt17 = Appointment(idnum=10, start="09:15", duration_in_mins=75,
                     patient=patient1, location=loc4, priority=105,
                     provider="Dr. Jane", interpreter='')
appt18 = Appointment(idnum=11, start="09:20", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=215,
                     provider="Dr. Jane", interpreter='')
appt19 = Appointment(idnum=12, start="09:50", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt20 = Appointment(idnum=13, start="10:00", duration_in_mins=35,
                     patient=patient1, location=loc5, priority=95,
                     provider="Dr. Jane", interpreter='')
appt21 = Appointment(idnum=14, start="10:00", duration_in_mins=35,
                     patient=patient1, location=loc4, priority=115,
                     provider="Dr. Jane", interpreter='')
appt22 = Appointment(idnum=15, start="10:00", duration_in_mins=105,
                     patient=patient1, location=loc4, priority=125,
                     provider="Dr. Jane", interpreter='')
appt23 = Appointment(idnum=16, start="10:10", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt24 = Appointment(idnum=17, start="10:15", duration_in_mins=45,
                     patient=patient1, location=loc5, priority=205,
                     provider="Dr. Jane", interpreter='')
appt25 = Appointment(idnum=18, start="10:15", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=85,
                     provider="Dr. Jane", interpreter='')
appt26 = Appointment(idnum=19, start="10:30", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt27 = Appointment(idnum=20, start="10:40", duration_in_mins=35,
                     patient=patient1, location=loc7, priority=115,
                     provider="Dr. Jane", interpreter='')
appt28 = Appointment(idnum=21, start="11:00", duration_in_mins=30,
                     patient=patient1, location=loc7, priority=115,
                     provider="Dr. Jane", interpreter='')
appt29 = Appointment(idnum=22, start="11:00", duration_in_mins=35,
                     patient=patient1, location=loc7, priority=205,
                     provider="Dr. Jane", interpreter='')
appt30 = Appointment(idnum=23, start="11:00", duration_in_mins=30,
                     patient=patient1, location=loc7, priority=205,
                     provider="Dr. Jane", interpreter='')
appt31 = Appointment(idnum=24, start="11:00", duration_in_mins=75,
                     patient=patient1, location=loc6, priority=212,
                     provider="Dr. Jane", interpreter='')
appt32 = Appointment(idnum=25, start="11:20", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=215,
                     provider="Dr. Jane", interpreter='')
appt33 = Appointment(idnum=26, start="12:15", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt34 = Appointment(idnum=27, start="12:30", duration_in_mins=45,
                     patient=patient1, location=loc4, priority=115,
                     provider="Dr. Jane", interpreter='')
appt35 = Appointment(idnum=28, start="12:45", duration_in_mins=30,
                     patient=patient1, location=loc5, priority=95,
                     provider="Dr. Jane", interpreter='')
appt36 = Appointment(idnum=29, start="12:55", duration_in_mins=75,
                     patient=patient1, location=loc6, priority=212,
                     provider="Dr. Jane", interpreter='')
appt37 = Appointment(idnum=30, start="13:00", duration_in_mins=45,
                     patient=patient1, location=loc7, priority=205,
                     provider="Dr. Jane", interpreter='')
appt38 = Appointment(idnum=31, start="13:00", duration_in_mins=45,
                     patient=patient1, location=loc7, priority=195,
                     provider="Dr. Jane", interpreter='')
appt39 = Appointment(idnum=32, start="13:00", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=215,
                     provider="Dr. Jane", interpreter='')
appt40 = Appointment(idnum=33, start="13:05", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt41 = Appointment(idnum=34, start="13:30", duration_in_mins=45,
                     patient=patient1, location=loc7, priority=212,
                     provider="Dr. Jane", interpreter='')
appt42 = Appointment(idnum=35, start="13:30", duration_in_mins=45,
                     patient=patient1, location=loc7, priority=195,
                     provider="Dr. Jane", interpreter='')
appt43 = Appointment(idnum=36, start="13:40", duration_in_mins=35,
                     patient=patient1, location=loc7, priority=115,
                     provider="Dr. Jane", interpreter='')
appt44 = Appointment(idnum=37, start="13:40", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=215,
                     provider="Dr. Jane", interpreter='')
appt45 = Appointment(idnum=38, start="13:45", duration_in_mins=75,
                     patient=patient1, location=loc6, priority=105,
                     provider="Dr. Jane", interpreter='')
appt46 = Appointment(idnum=39, start="13:55", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt47 = Appointment(idnum=40, start="14:00", duration_in_mins=135,
                     patient=patient1, location=loc6, priority=85,
                     provider="Dr. Jane", interpreter='')
appt48 = Appointment(idnum=41, start="14:00", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=85,
                     provider="Dr. Jane", interpreter='')
appt49 = Appointment(idnum=42, start="14:00", duration_in_mins=30,
                     patient=patient1, location=loc7, priority=85,
                     provider="Dr. Jane", interpreter='')
appt50 = Appointment(idnum=43, start="14:00", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt51 = Appointment(idnum=44, start="14:00", duration_in_mins=75,
                     patient=patient1, location=loc6, priority=212,
                     provider="Dr. Jane", interpreter='')
appt52 = Appointment(idnum=45, start="14:30", duration_in_mins=30,
                     patient=patient1, location=loc7, priority=75,
                     provider="Dr. Jane", interpreter='')
appt53 = Appointment(idnum=46, start="14:40", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=195,
                     provider="Dr. Jane", interpreter='')
appt54 = Appointment(idnum=47, start="15:00", duration_in_mins=55,
                     patient=patient1, location=loc4, priority=195,
                     provider="Dr. Jane", interpreter='')
appt55 = Appointment(idnum=48, start="15:00", duration_in_mins=55,
                     patient=patient1, location=loc5, priority=215,
                     provider="Dr. Jane", interpreter='')
appt56 = Appointment(idnum=49, start="15:30", duration_in_mins=30,
                     patient=patient1, location=loc6, priority=215,
                     provider="Dr. Jane", interpreter='')
appt57 = Appointment(idnum=50, start="16:00", duration_in_mins=45,
                     patient=patient1, location=loc6, priority=212,
                     provider="Dr. Jane", interpreter='')

bf_appts = [appt8, appt9, appt10, appt11, appt12,
            appt13, appt14, appt15, appt16, appt17, appt18, 
            appt19, appt20, appt21, appt22, appt23, appt24,
            appt25, appt26, appt27, appt28, appt29, appt30,
            appt31, appt32, appt33, appt34, appt35, appt36,
            appt37, appt38, appt39, appt40, appt41, appt42,
            appt43, appt44, appt45, appt46, appt47, appt48,
            appt49, appt50, appt51, appt52, appt53, appt54,
            appt55, appt56, appt57]

interpreters = [interpreter1, interpreter2, interpreter3]
appts = [appt1, appt2, appt3]
patients = [patient1, patient2]
test_schedule = Schedule(appts=appts,
                         interpreters=interpreters)
bf_test_schedule = Schedule(appts=bf_appts,
                            interpreters=interpreters)