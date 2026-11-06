
'''
Destination:
    1: Delhi
    2: Jaipur

When:
    1: Morning
    2: Afternoon
    3: Evening
    4: Night
'''

class RideRequest():
    def __init__(self, name, when_requested, destination=None, when=None, year=None):

        self.name = name
        self.destination = destination
        self.when = when
        self.year = year
        self.when_requested = when_requested

    def set_destination(self, destination):
        if destination != 1 and destination != 2:
            raise ValueError("Only two destinations are allowed. ")
        self.destination = destination

    def set_when(self, when):
        if when > 4 or when < 1:
            raise ValueError("Invalid time of trip")
        self.when = when

    def set_year(self, year):
        if year > 5 or year < 1:
            raise ValueError("Year can only be between 1 to 5.") 
        self.year = year



'''
seats: 1 to 4
destination and when are same as RideRequest
students is a list of students in it
'''
class Cab():
    def __init__(self, driver_name, seats, left, destination, when, students):

        if len(students) > seats:
            raise ValueError("Students should be less than seats in the cab.")

        if seats>4 or seats<1:
            raise ValueError("Seats can only be from 1 to 4.")

        if destination != 1 and destination != 2:
            raise ValueError("Only two destinations are allowed.")

        self.driver_name = driver_name
        self.seats = seats
        self.left = left
        self.destination = destination
        self.when = when
        self.students = students
