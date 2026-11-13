from colorama import init, Fore, Back, Style
import sys
import time
from classes import Cab, RideRequest
import os
from readchar import readchar, key
from utils import *
from collections import deque
import heapq
from persist import save_state, load_state

seq_no = 0
init(autoreset=True)


def clear_screen(ask=True):
    if ask:
        custom_input("\nPress Enter to return to the main menu...")
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print(Style.BRIGHT + Fore.CYAN + "CAB POOL MATCHER")
    print("\t1) Add new request")
    print("\t2) See everyone still waiting and all the cabs")
    print("\t3) Find matches (preview for all open cabs)")
    print("\t4) Dispatch a cab")
    print(Fore.RED + "\t5) Quit the app")

def get_action():
    while True:
        menu()
        print("\n\nEnter Option: ")
        c = readchar()

        if c == key.ESC:
            return 5

        if c == key.CTRL_C:
            print(Fore.RED + Style.BRIGHT + "\n\nCTRL C Detect!!! Exitting the code....")
            sys.exit(0)

        if c in ("1", "2", "3", "4", "5"):
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

def save():
    save_state(cabs, requests, seq_no)


def add_ride_request(request):
    key = (request.destination, request.when)
    global seq_no
    request.seq = seq_no
    seq_no += 1
    heapq.heappush(requests.setdefault(key, []), (-request.year, request.when_requested, request.seq, request))
    save()

    print(Fore.GREEN + "Request for ride added successfully...")
    if not open_cabs.get(key):
        print(Fore.YELLOW + "Note: no open cab for this trip right now. You will keep waiting until one is available.")


def print_all_requests():
    print(Fore.GREEN + "Printing all cab requests...")
    print("Total requests: " , sum(len(v) for v in requests.values()))
    print()

    for j in requests.values():
        for i in sorted(j):
            print_request(i[3])

def print_all_cabs():
    print(Fore.GREEN + "Printing all cabs...")
    print("Total cabs: ", len(cabs))
    print()

    for i in cabs:
        print_cab(i)
        
def preview_all_open_cabs():
    found_cab = False
    for key, dq in open_cabs.items():
        if not dq:
            continue
        for cab in dq:
            found_cab = True
            print_cab(cab)
            picks = [r for _, _, _, r in heapq.nsmallest(cab.free_seats(), requests.get(key, []))]
            if not picks:
                print(Fore.YELLOW + "\tNo one waiting for this cab.\n")
            for request in picks:
                print_request(request, fore_color_heading=Fore.GREEN, spacing=True)
    if not found_cab:
        print(Fore.YELLOW + "No open cabs.")


def pick_trip():
    print("Destinations: \n\t1: Delhi \n\t2: Jaipur")
    d = ask_number("Enter destination: ")
    if d is False:
        return None
    print()
    print("Time: \n\t1: Morning \n\t2: Afternoon \n\t3: Evening \n\t4: Night")
    t = ask_number("Pick time: ")
    if t is False:
        return None
    print()
    if d not in (1, 2) or t not in (1, 2, 3, 4):
        print(Fore.RED + "Invalid destination or time slot.")
        return None
    return (d, t)


def dispatch_cab():
    trip = pick_trip()
    if trip is None:
        return
    dq = open_cabs.get(trip)
    if not dq:
        print(Fore.RED + "No open cab for that trip. Nothing changed.")
        return
    heap = requests.get(trip, [])
    if not heap:
        print(Fore.RED + "Nobody is waiting for that trip. Nothing changed.")
        return
    cab = dq.popleft()
    while heap and cab.free_seats() > 0:
        cab.students.append(heapq.heappop(heap)[3])
    cab.left = True
    save()
    print(Fore.GREEN + "Cab dispatched!")
    if cab.free_seats():
        print(Fore.YELLOW + f"It left with {len(cab.students)}/{cab.seats} seats filled.")
    print_cab(cab)
    if heap:
        print(Fore.YELLOW + f"{len(heap)} student(s) still waiting for this trip.")


requests = {}
cabs = []
open_cabs = {}

clear_screen(ask=False)

cabs, open_cabs = read_cabs_from_csv('cabs.csv')

try:
    loaded = load_state(cabs)
    if loaded:
        requests, seq = loaded
        seq_no = seq
        open_cabs = {}
        for cab in cabs:
            if not cab.left:
                open_cabs.setdefault((cab.destination, cab.when), deque()).append(cab)
        print(Fore.GREEN + "Restored previous state from state.json.")
    else:
        print("No saved state found. Starting fresh.")
except Exception as err:
    print(Fore.RED + f"Saved state is missing or broken ({err}). Starting fresh.")
    for cab in cabs:
        cab.left, cab.students = False, []
    requests = {}
clear_screen()

while True:
    action = get_action()

    clear_screen(ask=False)

    if action == 5:
        save()
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

    if action == 4:
        dispatch_cab()

    clear_screen()

    