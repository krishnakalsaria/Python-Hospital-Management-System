class InvalidPatientIDError(Exception):
    pass


class InvalidAgeError(Exception):
    pass


class Person:
    def __init__(self, name, age):
        self.name = name

        if age < 0:
            raise InvalidAgeError("Invalid Age")

        self.age = age


class Patient(Person):
    def __init__(self, name, age, patient_id, disease):
        super().__init__(name, age)
        self.__patient_id = patient_id
        self.disease = disease

    def get_patient_id(self):
        return self.__patient_id

    def display_info(self):
        print("Patient Name:", self.name)
        print("Patient Age:", self.age)
        print("Patient ID:", self.__patient_id)
        print("Disease:", self.disease)


class InPatient(Patient):
    def __init__(self, name, age, patient_id, disease, room_no, days_admitted):
        super().__init__(name, age, patient_id, disease)
        self.room_no = room_no
        self.days_admitted = days_admitted


class OutPatient(Patient):
    def __init__(self, name, age, patient_id, disease, visit_date):
        super().__init__(name, age, patient_id, disease)
        self.visit_date = visit_date


class Doctor(Person):
    def __init__(self, name, age, doctor_id, specialization):
        super().__init__(name, age)
        self.__doctor_id = doctor_id
        self.specialization = specialization

    def get_doctor_id(self):
        return self.__doctor_id

    def display_info(self):
        print("Doctor Name:", self.name)
        print("Doctor Age:", self.age)
        print("Doctor ID:", self.__doctor_id)
        print("Specialization:", self.specialization)


class Hospital:

    def __init__(self):
        self.patients = []
        self.appointments = []


    def save_patients(self):
        with open("patients.txt", "w") as file:
            for patient in self.patients:
                file.write(
                    f"{patient.get_patient_id()},{patient.name},{patient.age},{patient.disease}\n"
                )


    def add_patient(self, patient):

        for p in self.patients:
            if p.get_patient_id() == patient.get_patient_id():
                print("Patient ID already exists")
                return

        self.patients.append(patient)

        with open("patients.txt", "a") as file:
            file.write(
                f"{patient.get_patient_id()},{patient.name},{patient.age},{patient.disease}\n"
            )

        print("Patient added successfully")


    def load_patients(self):

        try:
            with open("patients.txt", "r") as file:

                for line in file:

                    patient_id, name, age, disease = line.strip().split(",")

                    patient = Patient(
                        name,
                        int(age),
                        patient_id,
                        disease
                    )

                    self.patients.append(patient)

        except FileNotFoundError:
            pass



    def search_patient(self, patient_id):

        for patient in self.patients:

            if patient.get_patient_id() == patient_id:
                return patient

        raise InvalidPatientIDError("Patient ID not found")



    def update_patient(self, patient_id, new_disease):

        for patient in self.patients:

            if patient.get_patient_id() == patient_id:

                patient.disease = new_disease

                self.save_patients()

                print("Patient updated successfully")
                return

        print("Patient not found")



    def delete_patient(self, patient_id):

        for patient in self.patients:

            if patient.get_patient_id() == patient_id:

                self.patients.remove(patient)

                self.save_patients()

                print("Patient deleted successfully")
                return

        print("Patient not found")



    def book_appointments(self, name, patient_id, doctor_name, date, time):

        appointment = {
            "patient_name": name,
            "patient_id": patient_id,
            "doctor_name": doctor_name,
            "date": date,
            "time": time
        }

        self.appointments.append(appointment)

        print("Appointment booked successfully")



    def view_appointments(self):

        if len(self.appointments) == 0:
            print("No appointments found.")
            return

        print("\n===== Appointment Details =====")

        for appointment in self.appointments:

            print("Patient Name :", appointment["patient_name"])
            print("Patient ID   :", appointment["patient_id"])
            print("Doctor Name  :", appointment["doctor_name"])
            print("Date         :", appointment["date"])
            print("Time         :", appointment["time"])
            print("-------------------------------------")



    def generate_outpatient_bill(self, consultation_fee):

        print("----- OUTPATIENT BILL -----")
        print("Consultation Fee:", consultation_fee)
        print("Total Bill:", consultation_fee)
        print("-------------------------------------")



    def generate_inpatient_bill(self, room_charges, doctor_charges, medicine_charges):

        total = room_charges + doctor_charges + medicine_charges

        print("\n----- INPATIENT BILL -----")
        print("Room Charges:", room_charges)
        print("Doctor Charges:", doctor_charges)
        print("Medicine Charges:", medicine_charges)
        print("Total Bill:", total)
        print("-------------------------------------")



test_hospital = Hospital()

try:
    test_hospital.search_patient("P999")

except InvalidPatientIDError as e:
    print(e)



hospital = Hospital()

hospital.load_patients()

print(len(hospital.patients))


while True:

    print("===== Hospital Management System =====")
    print("1. Add Patient")
    print("2. Search Patient")
    print("3. Update Patient")
    print("4. Delete Patient")
    print("5. Book Appointment")
    print("6. View Appointments")
    print("7. Generate Bill")
    print("8. Exit")


    choice = input("Enter your choice: ")


    if choice == "1":

        try:

            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            patient_id = input("Enter Patient ID: ")
            disease = input("Enter Disease: ")

            patient = Patient(name, age, patient_id, disease)

            hospital.add_patient(patient)


        except InvalidAgeError as e:
            print(e)

        except ValueError:
            print("Age must be a number")



    elif choice == "2":

        try:

            patient_id = input("Enter Patient ID: ")

            patient = hospital.search_patient(patient_id)

            patient.display_info()


        except InvalidPatientIDError as e:

            print(e)



    elif choice == "3":

        patient_id = input("Enter Patient ID: ")

        new_disease = input("Enter New Disease: ")

        hospital.update_patient(patient_id, new_disease)



    elif choice == "4":

        patient_id = input("Enter Patient ID: ")

        hospital.delete_patient(patient_id)



    elif choice == "5":

        name = input("Enter Patient Name: ")
        patient_id = input("Enter Patient ID: ")
        doctor_name = input("Enter Doctor Name: ")
        date = input("Enter Date: ")
        time = input("Enter Time: ")


        hospital.book_appointments(
            name,
            patient_id,
            doctor_name,
            date,
            time
        )



    elif choice == "6":

        hospital.view_appointments()



    elif choice == "7":

        print("1. OutPatient Bill")
        print("2. InPatient Bill")


        bill_choice = input("Enter choice: ")


        if bill_choice == "1":

            consultation_fee = float(
                input("Enter Consultation Fee: ")
            )

            hospital.generate_outpatient_bill(
                consultation_fee
            )


        elif bill_choice == "2":

            room_charges = float(
                input("Enter Room Charges: ")
            )

            doctor_charges = float(
                input("Enter Doctor Charges: ")
            )

            medicine_charges = float(
                input("Enter Medicine Charges: ")
            )


            hospital.generate_inpatient_bill(
                room_charges,
                doctor_charges,
                medicine_charges
            )


        else:
            print("Invalid Choice")



    elif choice == "8":

        print("Thank You!")
        break



    else:

        print("Invalid Choice")