from copy import deepcopy

class Car:
    # Constants
    TYPES_OF_CAR = ("SUV", "Truck", "Mid size", "Luxury")
    TYPES_OF_FUEL = ("Gasoline", "Dieseal", "Electric")  # kept spelling for consistency

    def __init__(self, id, type, fuel, passengers, rent, avalible, year, name, picture):
        """
        Car object representing a vehicle in the system.
        """
        self.id = id
        self.type = type                # int index for TYPES_OF_CAR
        self.fuel = fuel                # int index for TYPES_OF_FUEL
        self.passengers = passengers
        self.rent = rent
        self.avl = avalible             # availability flag
        self.year = year
        self.name = name
        self.picture = picture          # optional picture ID

    # -------------------- Getters --------------------

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