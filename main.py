from colorama import init, Fore, Back, Style
import sys
import time
from classes import Cab, RideRequest
import os
from readchar import readchar, key
from utils import *
import heapq, itertools

counter = itertools.count()
init(autoreset=True)


def clear_screen(ask=True):
    if ask:
        custom_input("\nPress Enter to return to the main menu...")
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print(Style.BRIGHT + Fore.CYAN + "CAB POOL MATCHER")
    print("\t1) Add new request")
    print("\t2) See everyone still waiting and all the cabs")
    print("\t3) See previews for all cabs")
    print(Fore.RED + "\t4) Quit the app")

def get_action():
    while True:
        menu()
        print("\n\nEnter Option: ")
        c = readchar()

        if c == key.ESC:
            return 4

        if c == key.CTRL_C:
            print(Fore.RED + Style.BRIGHT + "\n\nCTRL C Detect!!! Exitting the code....")
            sys.exit(0)

        if c in ("1", "2", "3", "4"):
            print()
            return int(c)

        print(Fore.RED + "\nBad Option. Select again\n")


def ask_number(text):
    """Ask for a single digit. Returns an int, or False if Esc was pressed."""
    while True:
        c = custom_char(text)
        if c is False:
            return False
        if c in "0123456789" and c != "":
            return int(c)
        print(Fore.RED + "Please enter a number.")
        print()

def create_ride_request(retry=False):

    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "Hit escape to cancel this operation and return to main menu at any point of time.")

    if retry:
        print("Retrying adding new request...")
    else:
        print(Fore.GREEN + "Adding new ride request...")

    while True:
        name = custom_input("Enter name of the student: ")
        if name is False:
            return False
        name = name.strip()
        if name:
            break
        print(Fore.RED + "Name cannot be empty.")
        print()

    when_requested = time.time()

    request = RideRequest(name, when_requested)

    while True:
        print("Destinations: \n\t1: Delhi \n\t2: Jaipur")
        destination = ask_number("Enter your Destination: ")
        if destination is False:
            return False
        print()

        try:
            request.set_destination(destination)
            break
        except ValueError as err:
            print(Fore.RED + str(err))
            print()

    while True:
        print("Time: \n\t1: Morning \n\t2: Afternoon \n\t3: Evening \n\t4: Night")
        when = ask_number("Pick your time: ")
        if when is False:
            return False
        print()

        try:
            request.set_when(when)
            break
        except ValueError as err:
            print(Fore.RED + str(err))
            print()

    while True:
        year = ask_number("Enter which year student you are: ")
        if year is False:
            return False
        print()

        try:
            request.set_year(year)
            break
        except ValueError as err:
            print(Fore.RED + str(err))
            print()

    return request

def add_ride_request(request):
    key = (request.destination, request.when)
    heapq.heappush(requests.setdefault(key, []), (-request.year, request.when_requested, next(counter), request))

    print(Fore.GREEN + "Request for ride added successfully...")


def print_all_requests():
    print(Fore.GREEN + "Printing all cab requests...")
    print("Total requests: " , sum(len(v) for v in requests.values()))
    print()

    for j in requests.values():
        for i in j:
            print_request(i[3])

def print_all_cabs():
    print(Fore.GREEN + "Printing all cabs...")
    print("Total cabs: ", len(cabs))
    print()

    for i in cabs:
        print_cab(i)
        
def preview(cab):
    heap = requests.get((cab.destination, cab.when), [])
    top = heapq.nsmallest(cab.seats, heap)

    return [request for _, _, _, request in top]

def preview_all_open_cabs():
    for i in open_cabs.values():
        for j in i:
            print_cab(j)
            requests_local = preview(j)
            for request in requests_local:
                print_request(request, fore_color_heading=Fore.GREEN, spacing=True)


requests = {}
cabs = []
open_cabs = {}

clear_screen(ask=False)

cabs, open_cabs = read_cabs_from_csv('cabs.csv')
clear_screen()

while True:
    action = get_action()

    clear_screen(ask=False)

    if action == 4:
        print(Fore.GREEN + Style.BRIGHT + "Quitting APP....")
        sys.exit(0)

    if action == 1:
        request = create_ride_request()
        if not request:
            clear_screen(ask=False)
            continue
        add_ride_request(request)

    if action == 2:
        print_all_requests()
        print_all_cabs()

    if action == 3:
        preview_all_open_cabs()

    clear_screen()

    