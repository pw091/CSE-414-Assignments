from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import hashlib #I added this


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    '''create_patient <username> <password>'''
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        start()

    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        start()

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save the patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        start()
    print("Created user ", username)
    start()


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        start()

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        start()

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        start()
    print("Created user ", username)
    start()

def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    '''login_patient <username> <password>'''
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        start()

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        start()

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        start()

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient
    start()


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        start()

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        start()

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        start()

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver
    start()


def search_caregiver_schedule(tokens):
    '''search_caregiver_schedule <date>'''

    # check 1: if nobody is logged-in, they need to log in first
    if (current_caregiver is None) and (current_patient is None):
        print('Please login first!')
        start()
    
    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        start()

    date_string = tokens[1]
    try:
        date_tokens = date_string.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
        date = datetime.datetime(year, month, day)
    except: #check 3: imparsable date format
        print('Please try again!')
        start()

    #queries
    select_username =\
        '''
        SELECT A.Username
        FROM Availabilities A
        WHERE A.Time=%s
        ORDER BY A.Username;
        '''

    select_vaccines =\
        '''
        SELECT V.Name, V.Doses
        FROM Vaccines V;
        '''

    #execution
    def run_avail_query(query, date):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query, date)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching caregiver schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()
    
    def run_vaccine_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching vaccine schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()
    
    usernames = run_avail_query(select_username, date)
    vaccines = run_vaccine_query(select_vaccines)

    print('Caregiver Vaccine Doses:')
    for uname in usernames:
        for entry in vaccines:
            string = '{} {} {}'.format(uname['Username'], entry['Name'], entry['Doses'])
            print(string)
    start()

def reserve(tokens):
    '''reserve <date> <vaccine>'''
    #check 1: login null
    if (current_caregiver is None) and (current_patient is None):
        print('Please login first!')
        start()
    #check 2: login not patient
    if (current_caregiver is not None) and (current_patient is None): 
        print('Please login as patient!')
        start()
    #check 3: arg count
    if len(tokens) != 3:
        print("Please try again!")
        start()

    date_string = tokens[1]
    try:
        date_tokens = date_string.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
        date = datetime.datetime(year, month, day)
    except: #check 3: imparsable date format
        print('Please try again!')
        start()
    vacc = tokens[2]

    #----------------------------------------------------------

    #projection queries
    select_username =\
        '''
        SELECT A.Username
        FROM Availabilities A
        WHERE A.Time='{}'
        ORDER BY A.Username;
        '''.format(date)

    select_vacc_count=\
        '''
        SELECT V.Doses
        FROM Vaccines V
        WHERE V.Name='{}'
        '''.format(vacc)

    def run_avail_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching caregiver schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()
    
    def run_vacc_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching vaccine inventory")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    avail_caregivers = run_avail_query(select_username)
    if avail_caregivers==[]: #fail 1: no caregiver
        print('No Caregiver is available!')
        start()
    else:
        assigned_caregiver=avail_caregivers[0]['Username']

    avail_vacc_doses = run_vacc_query(select_vacc_count)
    if avail_vacc_doses==[]: #fail 2: bad vacc name
        print('Please try again!')
        start()
    if avail_vacc_doses[0]['Doses']==0: #fail 3: 0 doses
        print('Not enough available doses!')
        start()

    #------------------------------------------------------------
    appt_id = unique_identifier = hashlib.sha256((assigned_caregiver+str(date)).encode('utf-8')).hexdigest()[:255]

    #insertion query
    insert_appt =\
        '''
        INSERT INTO Appointments
        (Appointment_id, Time, Caregiver_uname, Patient_uname, Vaccine_name)
        VALUES
        ('{}','{}','{}','{}','{}')
        '''.format(appt_id, date, assigned_caregiver, current_patient.get_username(), vacc)
        
    def run_appt_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            conn.commit()
        except pymssql.Error as e:
            print("Error occurred when searching appointment schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    run_appt_query(insert_appt)

    #------------------------------------------------------------
    delete_avail =\
        '''
        DELETE
        FROM Availabilities
        WHERE (Username='{}' and Time='{}');
        '''.format(assigned_caregiver, date)

    def run_deletion_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            conn.commit()
        except pymssql.Error as e:
            print("Error occurred when updating availability")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    run_deletion_query(delete_avail)
    print('Appointment ID: {}, Caregiver username: {}'.format(appt_id, assigned_caregiver))
    start()

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        start()

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        start()

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        start()
    except ValueError:
        print("Please enter a valid date!")
        Start()
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        Start()
    print("Availability uploaded!")
    start()


def cancel(tokens):
    '''cancel <appointment_id>'''
    #check 1: login null
    if (current_caregiver is None) and (current_patient is None):
        print('Please login first!')
        start()
    
    #check 2: arg count
    if len(tokens) != 2:
        print("Please try again!")
        start() 

    appt_id = tokens[1]
    
    #Getters
    #--------------------------------
    #input validity
    select_appt_count =\
        '''
        SELECT count(*)
        FROM Appointments
        WHERE Appointment_id='{}';
        '''.format(appt_id)

    def run_count_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=False)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching appointments")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    apptExists = run_count_query(select_appt_count)[0][0]

    #check 3: arg validity
    if apptExists==0:
        print('Invalid appointment_id, please try again')
        start()
    
    #get time and caregiver
    select_appt_details =\
        '''
        SELECT Time, Caregiver_uname
        FROM Appointments
        WHERE Appointment_id='{}';
        '''.format(appt_id)

    def run_details_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching appointments")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    appt_details = run_details_query(select_appt_details)[0]
    date = appt_details['Time']
    caregiver = appt_details['Caregiver_uname']
    #Setters
    #-----------------------------------
    #delete appointment
    delete_appt =\
        '''
        DELETE
        FROM Appointments
        WHERE Appointment_id='{}';
        '''.format(appt_id)

    def run_deletion_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            conn.commit()
        except pymssql.Error as e:
            print("Error occurred when deleting appointment")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()
    run_deletion_query(delete_appt)
    
    #update_availability (time, uname)
    insert_avail =\
        '''
        INSERT INTO Availabilities
        VALUES ('{}','{}');
        '''.format(date, caregiver)

    def run_insertion_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            conn.commit()
        except pymssql.Error as e:
            print("Error occurred when searching appointment schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()
    
    run_insertion_query(insert_avail)
    print('Appointment cancelled successfully')
    start()

def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        start()

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        start()

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        start()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        start()

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            start()
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            start()
    print("Doses updated!")
    start()


def show_appointments(tokens):
    '''show_appointments (no args)'''
    #check 1: login null and 
    if (current_caregiver is None) and (current_patient is None):
        print('Please login first!')
        start()
    
    #caregiver or patient querying
    if current_caregiver is not None:
        user_arg = current_caregiver.get_username()
        select_arg = 'Patient_uname' #caregiver queries for patients
        filter_arg = 'Caregiver_uname'
    else:
        user_arg = current_patient.get_username()
        select_arg = 'Caregiver_uname' #patient queries for caregivers
        filter_arg = 'Patient_uname'

    #query string
    select_appts =\
        '''
        SELECT A.Appointment_id, A.Vaccine_name, A.Time, A.{}
        FROM Appointments A
        WHERE A.{}='{}'
        ORDER BY A.Appointment_id;
        '''.format(select_arg, filter_arg, user_arg)

    #execution
    def run_query(query):
        cm = ConnectionManager()
        conn = cm.create_connection()
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(query)
            return cursor.fetchall()
        except pymssql.Error as e:
            print("Error occurred when searching appointment schedule")
            print("Db-Error:", e)
            start()
        except Exception as e:
            print("Please try again!")
            print(e)
            start()
        finally:
            cm.close_connection()

    query_results = run_query(select_appts)
    if query_results==[]:
        print('{} has no appointments'.format(user_arg))
        start()
    headers = list(query_results[0].keys())
    print(' '.join(headers))
    for item in query_results:
        print(' '.join(str(item[key]) for key in headers))
    
    start()

def logout(tokens):
    '''logout (no args)'''
    global current_caregiver
    global current_patient
    #check 1
    if (current_caregiver is None) and (current_patient is None):
        print('Please login first!')
        start()
    elif current_caregiver is not None:
        current_caregiver=None
    else:
        current_patient=None
    print('Successfully logged out!')
    start()

def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == 'cancel': #I changed this
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
            exit() #I added this
        else:
            print("Invalid operation name!")
            start() #I added this


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
