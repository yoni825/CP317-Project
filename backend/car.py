from copy import deepcopy

class Car:
    # Constants
    TYPES_OF_CAR = ("SUV", "Truck", "Mid size", "Luxury")
    TYPES_OF_FUEL = ("Gasoline", "Dieseal", "Electric")  # kept spelling for consistency

def __init__(self, id, type, fuel, passengers, rent, avalible, year, name, picture):

    """
        ------------------------------------------------------
        initializes a class for Cars
        -------------------------------------------------------
        Parameters:
        id - int, id of the car
        type - int index representing type of car
        fuel - int index representing fuel type
        passengers - int, number of passengers
        rent - float, cost per day
        available - bool, whether car is available
        year - int, year manufactured
        name - str, name of the car
        -------------------------------------------------------
        """
    def getid(self):
        return self.id

    def gettype(self):
        try:
            return Car.TYPES_OF_CAR[self.type]
        except (IndexError, TypeError):
            return "Unknown"

    def getfuel(self):
        try:
            return Car.TYPES_OF_FUEL[self.fuel]
        except (IndexError, TypeError):
            return "Unknown"

    def getpassengers(self):
        return self.passengers

    def getrent(self):
        return self.rent

    def is_avalible(self):
        return self.avl

    def getyear(self):
        return self.year

    def getname(self):
        return self.name

    def getpicture(self):
        return self.picture

    # -------------------- Setters --------------------

    def set_availability(self, available: bool) -> None:
        """Updates availability of this car."""
        self.avl = available

    def set_rent(self, new_rent: float) -> None:
        """Updates rent of this car."""
        self.rent = new_rent