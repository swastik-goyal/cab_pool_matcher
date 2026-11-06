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
        header = next(reader)

        cabs = []
        open_cabs = {}

        for row in reader:

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



            cab = Cab(row[0], int(row[1]), False, row[2], row[3], [])

            cabs.append(cab)

        for cab in cabs:
            open_cabs.setdefault((cab.destination, cab.when), deque()).append(cab)

        print(Fore.GREEN + "Successfully fetched the cabs from CSV file.")
        return (cabs, open_cabs)

def print_cab(cab):
    print(Fore.YELLOW + "Driver Name: " + cab.driver_name)
    
    print("No of seats: ", cab.seats)

    if cab.left:
        print("Status: Already left")
    else:
        print("Status: Open")

    match cab.destination:
        case 1:
            print("Destination: Delhi")
        case 2:
            print("Destination: Jaipur")

    match cab.when:
        case 1:
            print("Time: Morning")
        case 2:
            print("Time: Afternoon")
        case 3:
            print("Time: Evening")
        case 4:
            print("Time: Night")
    
    print()

def print_request(request, fore_color_heading=Fore.YELLOW, spacing=False):

    if spacing:
        print('\t' + fore_color_heading + "Name: " + request.name)
            
        match request.destination:
            case 1:
                print('\t' + "Destination: Delhi")
            case 2:
                print('\t' + "Destination: Jaipur")
    
    
        match request.when:
            case 1:
                print('\t' + "Time: Morning")
            case 2:
                print('\t' + "Time: Afternoon")
            case 3:
                print('\t' + "Time: Evening")
            case 4:
                print('\t' + "Time: Night")
    
        print('\t' + "Year: ", request.year)
        print()

    else:

        print(fore_color_heading + "Name: " + request.name)
        
        match request.destination:
            case 1:
                print("Destination: Delhi")
            case 2:
                print("Destination: Jaipur")


        match request.when:
            case 1:
                print("Time: Morning")
            case 2:
                print("Time: Afternoon")
            case 3:
                print("Time: Evening")
            case 4:
                print("Time: Night")

        print("Year: ", request.year)
        print()