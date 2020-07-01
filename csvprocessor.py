import csv
from person import Patient
from location import Location
from schedule import Appointment


def csv_to_list(fh, newline='', delimiter=',', quote='|'):
    """Open a csv of tabular data and store its data in a list"""
    row_num = 0
    headers_dict = {}
    rows = {}
    with open(fh, newline=newline) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter,
                               quotechar=quote)
        for row in csvreader:
            row_num += 1
            if row_num <= 1:
                headers = row
                counter = 0
                for header in list(headers):
                    headers_dict[header] = counter
                    counter += 1
            rows[row_num - 1] = row
    return rows


def list_to_csv(rows, fh, newline='', delimiter=',', quote='|'):
    """Write a rows of tabular data to a csv"""
    with open(fh, 'w', newline=newline) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=delimiter,
                               quotechar=quote, quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csvwriter.writerow(rows[row])

            
def validate_int(arg):
    """Guard against value errors when attempting to
       convert a null to int"""
    if len(arg) < 1:
        return 0
    return int(arg)


def create_patient(headers_list, headers_dict, data):
    """Assumes headers_list is in the order:
      [pat_id, pat_name, pat_lang, pat_gender]"""
    # get headers
    pat_id_pos = headers_dict[headers_list[0]]
    pat_name_pos = headers_dict[headers_list[1]]
    pat_lang_pos = headers_dict[headers_list[2]]
    pat_gender_pos = headers_dict[headers_list[3]]
    # get data
    pat_id = data[pat_id_pos]
    pat_name = data[pat_name_pos]
    pat_lang = {data[pat_lang_pos]}
    pat_gender = data[pat_gender_pos]
    return Patient(pat_id, pat_name, pat_lang, pat_gender)


def create_location(headers_list, headers_dict, data):
    """ Assumes headers_list is in the order:
       [location_x_coord, location_y_coord, bldg, clinic]"""
    # get headers
    location_x_coord_pos = headers_dict[headers_list[0]]
    location_y_coord_pos = headers_dict[headers_list[1]]
    bldg_pos = headers_dict[headers_list[2]]
    clinic_pos = headers_dict[headers_list[3]]
    # get data
    location_x_coord = validate_int(data[location_x_coord_pos])
    location_y_coord = validate_int(data[location_y_coord_pos])
    bldg = data[bldg_pos]
    clinic = data[clinic_pos]
    return Location(location_x_coord, location_y_coord, bldg, clinic)

    
def create_appointment(pat_list, loc_list, headers_list,
                       headers_dict, data):
    """Assumes headers_list is in the order:
       [appointment_id, start, duration, priority, provider, interpreter]"""
    # get headers
    appointment_id_pos = headers_dict[headers_list[0]]
    start_pos = headers_dict[headers_list[1]]
    duration_pos = headers_dict[headers_list[2]]
    priority_pos = headers_dict[headers_list[3]]
    provider_pos = headers_dict[headers_list[4]]
    interpreter_pos = headers_dict[headers_list[5]]
    # get data
    appointment_id = validate_int(data[appointment_id_pos])
    start = data[start_pos]
    duration = validate_int(data[duration_pos])
    priority = validate_int(data[priority_pos])
    provider = data[provider_pos]
    interpreter = data[interpreter_pos]
    # create dependant objects
    pat = create_patient(pat_list, headers_dict, data)
    loc = create_location(loc_list, headers_dict, data)
    
    return Appointment(appointment_id, start, duration, pat, loc,
                       priority, provider, interpreter)
