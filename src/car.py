from copy import deepcopy

class Car:
    # Constants
    TYPES_OF_CAR = ("SUV", "Truck", "Mid size", "Luxury")
    TYPES_OF_FUEL = ("Gasoline", "Dieseal", "Electric")  # kept spelling to match rest of code

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
            avalible - bool, whether car is available
            year - int, year manufactured
            name - str, name of the car
            picture - int, id for picture of car
        -------------------------------------------------------
        """
        self.id = deepcopy(id)
        self.type = deepcopy(type)          # int index into TYPES_OF_CAR
        self.fuel = deepcopy(fuel)          # int index into TYPES_OF_FUEL
        self.passen = deepcopy(passengers)
        self.rent = deepcopy(rent)
        self.avl = deepcopy(avalible)
        self.year = deepcopy(year)
        self.name = deepcopy(name)
        self.pic = deepcopy(picture)

    def getid(self):
        """Returns id of car (int)."""
        return deepcopy(self.id)

    def gettype(self):
        """
        Returns car type as a STRING, e.g. 'SUV', 'Truck', etc.
        """
        try:
            return deepcopy(self.TYPES_OF_CAR[self.type])
        except (IndexError, TypeError):
            return "Unknown"

    def getfuel(self):
        """
        Returns fuel type as a STRING: 'Gasoline', 'Dieseal', 'Electric'.
        """
        try:
            return deepcopy(self.TYPES_OF_FUEL[self.fuel])
        except (IndexError, TypeError):
            return "Unknown"

    def getpassengers(self):
        """Returns number of passengers (int)."""
        return deepcopy(self.passen)

    def getrent(self):
        """Returns rent price per day (float)."""
        return deepcopy(self.rent)

    def is_avalible(self):
        """Returns availability (bool)."""
        return deepcopy(self.avl)

    def getyear(self):
        """Returns manufacture year (int)."""
        return deepcopy(self.year)

    def getname(self):
        """Returns car name (string)."""
        return deepcopy(self.name)

    def getpicture(self):
        """Returns picture id (int)."""
        return deepcopy(self.pic)

    def set_availability(self, available: bool) -> None:
        """Sets the availability of the car."""
        self.avl = deepcopy(available)
