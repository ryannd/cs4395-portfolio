# Portfolio Assignment 1: Text Processing with Python
# Ryan Dimaranan rtd180003
# CS 4395.001

import sys
import os
import re
import pickle

# Person class to store information 
class Person:
    def __init__(self, last, first, mi, iD, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.iD = iD
        self.phone = phone
    # displays the person's information
    def display(self):
        print(f'Employee ID: {self.iD}')
        print(f'\t{self.first} {self.mi} {self.last}')
        print(f'\t{self.phone}\n')

# Parses CSV file
def parse_input_file(file_content):
    person_dict = {} # dict to store Person objects
    idRegex = r"^[a-zA-Z]{2}\d{4}$" # regex to ensure id meets requirements 
    phoneRegex = r"^(\d{3}).?(\d{3}).?(\d{4})$" # regex to ensure valid phone number

    # parse each line in csv file
    for line in file_content:
        person_fields = line.split(',')
        # get attributes from line
        last = person_fields[0].capitalize()
        first = person_fields[1].capitalize()
        mi = person_fields[2][0].upper() if person_fields[2] else "X"
        iD = person_fields[3]
        # ensure non duplicate ID and valid ID
        while not re.search(idRegex, iD) or iD in person_dict.keys():
            if iD in person_dict.keys():
                iD = input(f"Employee ID {iD} exists. Enter new ID: ")
            else:
                iD = input(f"Employee ID {iD} invalid. Enter new ID: ")
        # ensure valid phone number, normalize to xxx-xxx-xxxx format
        phone_parse = re.search(phoneRegex, person_fields[4])
        while phone_parse is None:
            new_phone = input(f"Phone number for ID {iD} is invalid. Enter new phone number: ")
            phone_parse = re.search(phoneRegex, new_phone)
        phone_groups = phone_parse.groups()
        phone = f"{phone_groups[0]}-{phone_groups[1]}-{phone_groups[2]}"
        # create Person object
        curr_person = Person(last,first,mi,iD,phone)
        # duplicate ID check
        if iD in person_dict.keys():
            print(f"Person with ID {iD} already exists.")
        else:
            person_dict[iD] = curr_person
    
    # save to pickle file
    pickle.dump(person_dict, open('person_dict.p', 'wb'))

def main():
    # check if filepath was entered
    if len(sys.argv) < 2:
        print("No file name specified.")
    else:
        path = sys.argv[1]
        # check if file exists
        try:
            with open(os.path.join(os.getcwd(), path), 'r') as f:
                file_content = f.read().splitlines()
                file_content.pop(0)
        except FileNotFoundError:
            print("File not found. Re-run the program with a different filepath.")
            return
        # parse input file and save resulting dict to pickle file
        parse_input_file(file_content)
        
        # read pickle file and display each person stored
        pickle_dict = pickle.load(open('person_dict.p','rb'))
        print("\nEmployee list:\n")
        for person in pickle_dict.values():
            person.display()
        

if __name__ == '__main__':
    main()