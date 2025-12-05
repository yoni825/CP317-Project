"""
-------------------------------------------------------
[Reservation functions - Backend]
-------------------------------------------------------
This file contains the Reservation class and functions
to handle car reservations in the Car Rental System.

- Stores reservations persistently in data/reservations.json
- Links each reservation to a Car object by car_id
- Marks reserved cars as unavailable
-------------------------------------------------------
"""

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import json

# Path to the persistent reservations file (data folder)
DATA_DIR = Path("data")
RESERVATION_FILE = DATA_DIR / "reservations.json"


class Reservation:
    """
    Stores reservation information.
    """
    def __init__(self, res_id, user_name, car, start_date, end_date, total_price):
        self.res_id = deepcopy(res_id)
        self.user_name = deepcopy(user_name)
        self.car = car
        self.start_date = deepcopy(start_date)
        self.end_date = deepcopy(end_date)
        self.total_price = deepcopy(total_price)

    def to_dict(self):
        """
        Convert object to a JSON-safe dict.
        Car object becomes just car_id.
        """
        return {
            "res_id": self.res_id,
            "user_name": self.user_name,
            "car_id": self.car.getid(),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_price": self.total_price,
        }

    @staticmethod
    def from_dict(data, cars_by_id):
        """
        Convert JSON dict back into a Reservation.

        cars_by_id: dict[int, Car]
            Mapping from car ID to Car object.
        """
        car = cars_by_id.get(data["car_id"])
        if car is None:
            # If the referenced car doesn't exist anymore, skip this reservation.
            return None

        start = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

        return Reservation(
            data["res_id"],
            data["user_name"],
            car,
            start,
            end,
            data["total_price"],
        )



def save_reservations(reservations):
    """
    Save reservations list to data/reservations.json.
    """
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    with open(RESERVATION_FILE, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in reservations], f, indent=4)


def load_reservations(cars):
    """
    Load reservations from JSON and attach cars by id.
    Also marks reserved cars as unavailable (simple logic).

    cars: list[Car]
        Existing car objects used to link car_id → Car.
    """
    if not RESERVATION_FILE.exists():
        return []

    with open(RESERVATION_FILE, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            return []

    cars_by_id = {c.getid(): c for c in cars}
    reservations = []

    for item in raw:
        res = Reservation.from_dict(item, cars_by_id)
        if res is not None:
            reservations.append(res)
            res.car.avl = False

    return reservations



def reserve_car(cars, reservations, car_id, user_name, start_str, end_str):
    """
    Create a reservation if possible and save it.

    Returns:
        Reservation object on success, or None on failure.
    """
    # Parse dates
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        # Invalid date format
        return None

    # Check date range
    if end_date < start_date:
        return None

    # Find selected car
    selected_car = None
    for c in cars:
        if c.getid() == car_id:
            selected_car = c
            break

    if selected_car is None:
        # No car with that ID
        return None

    if not selected_car.is_avalible():
        # Car already reserved / unavailable
        return None

    # Compute total price
    days = (end_date - start_date).days + 1
    total_price = days * selected_car.getrent()

    # New reservation ID (simple incremental)
    new_id = len(reservations) + 1

    reservation = Reservation(
        new_id,
        user_name,
        selected_car,
        start_date,
        end_date,
        total_price,
    )
    reservations.append(reservation)

    # Mark car unavailable
    selected_car.avl = False

    # Persist to file
    save_reservations(reservations)

    return reservation


# -------------------- History Helpers -------------------- #

def get_user_reservations(reservations, user_name):
    """
    Return a list of reservations for a given user.
    """
    return [r for r in reservations if r.user_name == user_name]


def get_all_reservations(reservations):
    """
    Return a copy of all reservations.
    """
    return list(reservations)
