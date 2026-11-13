from readchar import readchar, key
import csv
from classes import Cab
from colorama import Fore, Style, init
from collections import deque
import sys

init(autoreset=True)

def custom_input(text=None):
    if text:
        print(text, end='')
    s = ""
    while True:
        c = readchar()
        if c==key.ESC:
            return False
        if c==key.ENTER:
            print()
            return s

        if c==key.CTRL_C:
            print(Fore.RED + Style.BRIGHT + "\n\nCTRL C Detect!!! Exitting the code....")
            sys.exit(0)
        
        s += c
        print(c, end='')


def custom_char(text=None):
    if text:
        print(text, end='')
    c = readchar()
    if c==key.ESC:
        return False
    if c==key.CTRL_C:
        print(Fore.RED + Style.BRIGHT + "\n\nCTRL C Detect!!! Exitting the code....")
        sys.exit(0)
    print(c)
    return c


def read_cabs_from_csv(path='cabs.csv'):
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)

        cabs = []
        open_cabs = {}

        for row in reader:
            if len(row) < 4:
                continue

            if row[2].lower() == 'delhi':
                row[2] = 1
            elif row[2].lower() == 'jaipur':
                row[2] = 2
            else:
                print(Fore.RED + "Invalid destination detected. Skipping this cab entry...")
                continue


            if row[3].lower() == 'morning':
                row[3] = 1
            elif row[3].lower() == 'afternoon':
                row[3] = 2
            elif row[3].lower() == 'evening':
                row[3] = 3
            elif row[3].lower() == 'night':
                row[3] = 4
            else:
                print(Fore.RED + "Invalid time detected. Skipping this cab entry...")
                continue



            try:
                cab = Cab(row[0], int(row[1]), False, row[2], row[3], [])
            except ValueError as err:
                print(Fore.RED + f"Skipping bad cab row {row[0]!r}: {err}")
                continue

            cabs.append(cab)

        for cab in cabs:
            open_cabs.setdefault((cab.destination, cab.when), deque()).append(cab)

        print(Fore.GREEN + "Successfully fetched the cabs from CSV file.")
        return (cabs, open_cabs)

DEST_NAMES = {1: "Delhi", 2: "Jaipur"}
TIME_NAMES = {1: "Morning", 2: "Afternoon", 3: "Evening", 4: "Night"}


def print_cab(cab):
    print(Fore.YELLOW + "Driver Name: " + cab.driver_name)
    print(f"Seats: {len(cab.students)}/{cab.seats}")
    print("Status: " + ("Already left" if cab.left else "Open"))
    print("Destination:", DEST_NAMES[cab.destination])
    print("Time:", TIME_NAMES[cab.when])
    if cab.students:
        print("Passengers:", ", ".join(f"{s.name} (Y{s.year})" for s in cab.students))
    print()


def print_request(request, fore_color_heading=Fore.YELLOW, spacing=False):
    p = '\t' if spacing else ''
    print(p + fore_color_heading + "Name: " + request.name)
    print(p + "Destination:", DEST_NAMES[request.destination])
    print(p + "Time:", TIME_NAMES[request.when])
    print(p + "Year:", request.year)
    print()
