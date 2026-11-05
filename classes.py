
'''
Destination:
    0: Delhi
    1: Jaipur

When:
    0: Morning
    1: Afternoon
    2: Evening
    3: Night
'''
class RideRequest():
    def __init__(self, name, destination, when, year, when_requested):

        if year > 5 or year < 0:
            raise ValueError("Year can only be between 1 to 5.") 

        if destination != 0 and destination != 1:
            raise ValueError("Only two destinations are allowed. ")

        self.name = name
        self.destination = destination
        self.when = when
        self.year = year
        self.when_requested = when_requested


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

        if destination != 0 and destination != 1:
            raise ValueError("Only two destinations are allowed.")

        self.driver_name = driver_name
        self.seats = seats
        self.left = left
        self.destination = destination
        self.when = when
        self.students = students
