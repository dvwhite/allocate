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

loc1 = Location(x=0,
                y=0,
                building="Central Hospital",
                clinic="Radiology")

loc2 = Location(x=4,
                y=-4,
                building="West Wing",
                clinic="Ophthalmology")

loc3 = Location(x=3,
                y=4,
                building="East Wing",
                clinic="Emergency Room")

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

interpreters = [interpreter1, interpreter2, interpreter3]
appts = [appt1, appt2, appt3]
patients = [patient1, patient2]
test_schedule = Schedule(appts=appts,
                         interpreters=interpreters)
