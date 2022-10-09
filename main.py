import re
import pandas as pd
import csv
import hashlib


def login():
    config_data = []
    with open('config.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            config_data.append(row)

    count = 0
    username = ""
    password = ""
    password_check = ""

    while username == "":
        if count > 0:
            print(str(5 - count) + " more attempts remaining...")
        print("Enter Username:")
        user_input = input().strip()
        if user_input not in [i[0] for i in config_data]:
            if count > 3:
                print("Invalid Username\nToo many attempts taken!!!")
                return
            print("Invalid Username\nDo you want to Continue SignIn?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                count += 1
                continue
            elif i == 0:
                break
        else:
            username = user_input
            count = 0

    for cd in config_data:
        if cd[0] == username:
            password_check = cd[1]

    while username != "" and password == "":
        if count > 0:
            print(str(5 - count) + " more attempts remaining...")
        print("Enter Password:")
        pass_input = input().strip()
        if hashlib.md5(pass_input.encode()).hexdigest() == password_check:
            password = pass_input
            print("Successfully Logged in")
        else:
            if count > 3:
                print("Incorrect Password\nToo many attempts taken!!!")
                return
            print("Incorrect Password\nDo you want to Continue SignIn?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                count += 1
                continue
            elif i == 0:
                break

    if username != "" and password != "":
        data = []
        for cd in config_data:
            if cd[0] == username:
                data.append(cd[2])
                data.append(cd[3])

        if data[1] == 'staff':
            staff_session(int(data[0]))
        elif data[1] == 'patient':
            patient_session(int(data[0]), username)


def register():
    config_data = []
    with open('config.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            config_data.append(row)

    data = []

    privilege_level = 0
    username = ""
    password = ""
    role = ""

    while role == "":
        print("Select Role\n1-HOSPITAL STAFF\n2-PATIENT")
        r = input().strip()
        if r == '1':
            role = 'staff'
        elif r == '2':
            role = 'patient'
        else:
            print("Incorrect Inputs.\nDo you want to Continue Register?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                continue
            elif i == 0:
                break

    while username == "" and role != "":
        print("Enter Username:")
        user_input = input().strip()
        if user_input in [i[0] for i in config_data]:
            print("Already Existing Username\nDo you want to Continue Register?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                continue
            elif i == 0:
                break
        else:
            if len(user_input) < 5:
                print("Username should be at least 5 characters\nDo you want to Continue Register?\n1-YES\n0-NO")
                i = int(input())
                if i == 1:
                    continue
                elif i == 0:
                    break
            else:
                username = user_input
                data.append(username)

    while username != "" and password == "" and role != "":
        print("Enter Password:")
        pass_input = input().strip()
        if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", pass_input):
            print("Re-Enter Password:")
            repass_input = input().strip()
            if pass_input == repass_input:
                password = hashlib.md5(pass_input.encode()).hexdigest()
                data.append(password)
            else:
                print("Password mismatched!\nDo you want to Continue Register?\n1-YES\n0-NO")
                i = int(input())
                if i == 1:
                    continue
                elif i == 0:
                    break
        else:
            if len(pass_input) < 8:
                print("Password should be minimum 8 characters!\nDo you want to Continue Register?\n1-YES\n0-NO")
            else:
                print("Password should contain at least one uppercase letter, one lowercase letter, one digit and "
                      "one special character!\nDo you want to Continue Register?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                continue
            elif i == 0:
                break

    while username != "" and password != "" and privilege_level == 0 and role == "staff":
        print("Select Role:"
              "\n1 - DOCTOR\n2 - NURSE\n3 - PHARMACIST"
              "\n4 - MEDICAL LABORATORY TECHNICIAN\n5 - RECEPTIONIST")

        r = input().strip()

        code = ""
        if r in ['1', '2', '3', '4', '5']:
            print("Enter Verification Code:")
            code = input().strip()

        if r == '1' and code == 'doc1111':
            privilege_level = 1
            data.append(privilege_level)
        elif r == '2' and code == 'nur2222':
            privilege_level = 2
            data.append(privilege_level)
        elif r == '3' and code == 'pharm33':
            privilege_level = 3
            data.append(privilege_level)
        elif r == '4' and code == 'mlt4444':
            privilege_level = 4
            data.append(privilege_level)
        elif r == '5' and code == 'recep55':
            privilege_level = 5
            data.append(privilege_level)
        else:
            print("Enter correct values\nDo you want to Continue Register?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                continue
            elif i == 0:
                break

    if role == 'patient':
        data.append(6)

    data.append(role)
    if len(data) == 4:
        config_data.append(data)
        with open('config.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(config_data)
        print("Successfully Registered")


def view_all_details(privilege_level):
    with open("data.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            print("---------------------------------------------------------------------")
            print("Patient                :" + dict(row)["patient"])
            if privilege_level == 1 or privilege_level == 2:
                print("Sickness Details       :" + dict(row)["sickness details"])
            if privilege_level == 1 or privilege_level == 3:
                print("Drug Prescriptions     :" + dict(row)["drug prescriptions"])
            if privilege_level == 1 or privilege_level == 4:
                print("Lab Test Prescriptions :" + dict(row)["lab test prescriptions"])
            if privilege_level == 1 or privilege_level == 5:
                print("Personal Details       :" + dict(row)["personal details"])
            print("---------------------------------------------------------------------")


def view_patient_details(privilege_level, patient):
    with open("data.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if dict(row)["patient"] == patient:
                print("---------------------------------------------------------------------")
                if privilege_level != 6:
                    print("Patient                :" + dict(row)["patient"])
                if privilege_level == 1 or privilege_level == 6 or privilege_level == 2:
                    print("Sickness Details       :" + dict(row)["sickness details"])
                if privilege_level == 1 or privilege_level == 6 or privilege_level == 3:
                    print("Drug Prescriptions     :" + dict(row)["drug prescriptions"])
                if privilege_level == 1 or privilege_level == 6 or privilege_level == 4:
                    print("Lab Test Prescriptions :" + dict(row)["lab test prescriptions"])
                if privilege_level == 1 or privilege_level == 6 or privilege_level == 5:
                    print("Personal Details       :" + dict(row)["personal details"])
                print("---------------------------------------------------------------------")
                break
        else:
            print("----- No records found -----")


def add_details(patient, detail):
    columns = ['patient', 'personal details', 'sickness details', 'drug prescriptions', 'lab test prescriptions']
    row = {'patient': patient, 'sickness details': "", 'drug prescriptions': "", 'personal details': "",
           'lab test prescriptions': ""}
    print("Enter " + detail.upper() + " :")
    data_in = input().strip()
    row.update({detail: data_in})
    with open('data.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=columns)
        dictwriter_object.writerow(row)
        f_object.close()


def edit_details(patient, detail):
    if patient in pd.read_csv('data.csv')['patient'].tolist():
        d = pd.read_csv('data.csv', index_col='patient').loc[patient, detail]
        if not pd.isna(d):
            print("---------------------------------------------------------------------")
            print("Patient: " + patient + "\n" + detail.upper() + " : " + d)
            print("---------------------------------------------------------------------")
            print("Do you want to edit details?\n1-YES\n0-NO")
            i = int(input())
            if i == 1:
                print("Enter new details:")
                new_data = input().strip()
                print("Do you want to keep old details?\n1-YES\n0-NO")
                j = int(input())
                if j == 1:
                    data = d + ' , ' + new_data
                    df = pd.read_csv('data.csv', index_col='patient')
                    df.loc[patient, detail] = data
                    df.to_csv('data.csv')
                elif j == 0:
                    df = pd.read_csv('data.csv', index_col='patient')
                    df.loc[patient, detail] = new_data
                    df.to_csv('data.csv')

            elif i == 0:
                return

        else:
            print("No records Found\nDo you want to add record?\n1-YES\n0-NO")
            j = int(input())
            if j == 1:
                print("Enter new details:")
                new_data = input().strip()
                df = pd.read_csv('data.csv', index_col='patient')
                df.loc[patient, detail] = new_data
                df.to_csv('data.csv')

            elif j == 0:
                return

    else:
        print("No records Found\nDo you want to add record?\n1-YES\n0-NO")
        j = int(input())
        if j == 1:
            add_details(patient, detail)
        elif j == 0:
            return


def edit_patient_details(privilege_level, patient):
    if privilege_level == 1:
        flag = True
        while flag:
            print("Select detail type to Edit:\n1 - Sickness Details\n2 - Drug Prescriptions"
                  "\n3 - Lab Test Prescriptions\n4 - Personal Details\n0 - exit")
            sel_input = input().strip()
            if sel_input == '1':
                edit_details(patient, 'sickness details')
            elif sel_input == '2':
                edit_details(patient, 'drug prescriptions')
            elif sel_input == '3':
                edit_details(patient, 'lab test prescriptions')
            elif sel_input == '4':
                edit_details(patient, 'personal details')
            elif sel_input == '0':
                flag = False
            else:
                print("Enter Valid Input.\nDo you want to continue?\n1-YES\n0-NO")
                i = int(input())
                if i == 1:
                    continue
                elif i == 0:
                    flag = False
                    break
    elif privilege_level == 2:
        edit_details(patient, 'sickness details')
    elif privilege_level == 3:
        edit_details(patient, 'drug prescriptions')
    elif privilege_level == 4:
        edit_details(patient, 'lab test prescriptions')
    elif privilege_level == 5:
        edit_details(patient, 'personal details')


def staff_session(privilege_level):
    while True:
        print("Select Functionality:\n1 - VIEW DETAILS - all patients\n2 - VIEW DETAILS - selected patients"
              "\n3 - EDIT DETAILS - selected patient\n00-LOGOUT")
        i = input().strip()

        if i == '1':
            view_all_details(privilege_level)
        elif i == '2' or i == '3':
            config_data = []
            with open('config.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    config_data.append(row)

            patient = ""
            while patient == "":
                print("Enter patient username:")
                patient_input = input().strip()
                if patient_input not in [i[0] for i in config_data]:
                    print("Invalid Patient.\nDo you want to continue?\n1-YES\n0-NO")
                    j = int(input())
                    if j == 1:
                        continue
                    elif j == 0:
                        break
                else:
                    patient = patient_input

            if i == '2' and patient != "":
                view_patient_details(privilege_level, patient)

            if i == '3' and patient != "":
                edit_patient_details(privilege_level, patient)
        elif i == '00':
            break
        else:
            print("Enter Correct Input")


def patient_session(privilege_level, username):
    while True:
        print("Select Functionality:\n1 - VIEW DETAILS\n00-LOGOUT")
        i = input().strip()

        if i == '1':
            view_patient_details(privilege_level, username)
        elif i == '00':
            break
        else:
            print("Enter Correct Input")


while True:
    print("Select Functionality:\n1 - LOGIN\n2 - REGISTER\n0 - exit")
    func = input().strip()
    if func == '0':
        print("Good Bye...")
        break
    elif func == '1':
        print("SignIn")
        login()
    elif func == '2':
        print("Register")
        register()
    else:
        print("Enter correct value")
