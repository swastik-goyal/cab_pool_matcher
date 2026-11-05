from colorama import init, Fore, Back, Style
import sys
import time
from classes import Cab, RideRequest
import os
from readchar import readchar, key
from utils import custom_input

init(autoreset=True)

def clear_screen(ask=True):
    if ask:
        input("\nPress Enter to return to the main menu...")
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print(Style.BRIGHT + Fore.CYAN + "CAB POOL MATCHER")
    print("\t1) Add new request")
    print("\t2) See everyone still waiting and all the cabs")
    print(Fore.RED + "\t3) Quit the app")

def get_action():
    menu()
    print("\n\nEnter Option: ")
    action = int(readchar())
    print()

    if action > 3 or action < 1:
        print(Fore.RED + "Bad Option. Select again\n")
        action = get_action()


    return action

def add_ride_request(retry=False):

    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "Hit escape to cancel this operation and return to main menu at any point of time.")

    if retry:
        print("Retrying adding new request...")
    else:
        print(Fore.GREEN + "Adding new ride request...")

    name = custom_input("Enter name of the student: ")
    if not name:
        return False

    print("Destinations: \n\t0: Delhi \n\t1: Jaipur")
    destination = int(input("Enter your Destination: "))
    print()

    print("Time: \n\t0: Morning \n\t1: Afternoon \n\t2: Evening \n\t3: Night")
    when = int(input("Pick your time: "))
    print()

    year = int(input("Enter which year student you are: "))
    when_requested = time.time()

    try:
        request = RideRequest(name, destination, when, year, when_requested)
        print(Fore.GREEN + "Request successfully created...")
        return request
    except ValueError as err:
        print(Fore.RED + str(err))
        return add_ride_request(retry=True)
    except:
        print(Fore.RED + "Something went wrong...")
        return add_ride_request(retry=True)

def print_all_requests():
    print(Fore.LIGHTYELLOW_EX + "Printing all cab requests...")
    print("Total requests: " , len(requests))
    print()

    for i in requests:
        print("Name: ", i.name)

        match i.destination:
            case 0:
                print("Destination: Delhi")
            case 1:
                print("Destination: Jaipur")

        match i.when:
            case 0:
                print("Time: Morning")
            case 1:
                print("Time: Afternoon")
            case 2:
                print("Time: Evening")
            case 3:
                print("Time: Night")

        print("Year: ", i.year)
        print()




requests = []
cabs = []

clear_screen(ask=False)

while True:
    action = get_action()

    clear_screen(ask=False)

    if action == 3:
        print(Fore.GREEN + Style.BRIGHT + "Quitting APP....")
        sys.exit(0)

    if action == 1:
        request = add_ride_request()
        if not request:
            clear_screen(ask=False)
            continue
        requests.append()

    if action == 2:
        print_all_requests()

    clear_screen()

    