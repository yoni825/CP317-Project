"""
-------------------------------------------------------
[Reservation functions]
-------------------------------------------------------
This file contains the Reservation class and functions
to handle car reservations in the Car Rental System.
-------------------------------------------------------
"""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import json

# File where persistent reservations are stored
RESERVATION_FILE = Path("reservations.json")


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
            "total_price": self.total_price
        }

    @staticmethod
    def from_dict(data, cars_by_id):
        """
        Convert JSON dict back into a Reservation.
        """
        car = cars_by_id.get(data["car_id"])
        if car is None:
            return None  # Ignore corrupted references

        start = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

        return Reservation(
            data["res_id"],
            data["user_name"],
            car,
            start,
            end,
            data["total_price"]
        )


# -------------------- Persistence --------------------

def save_reservations(reservations):
    """
    Save reservations list to reservations.json.
    """
    with open(RESERVATION_FILE, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in reservations], f, indent=4)


def load_reservations(cars):
    """
    Load reservations from JSON and attach cars by id.
    Also marks reserved cars as unavailable (simple logic).
    """
    if not RESERVATION_FILE.exists():
        return []

    with open(RESERVATION_FILE, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            return []  # corrupted/empty file → ignore

    cars_by_id = {c.getid(): c for c in cars}
    reservations = []

    for item in raw:
        res = Reservation.from_dict(item, cars_by_id)
        if res is not None:
            reservations.append(res)
            res.car.avl = False  # SIMPLE rule: reserved once = not available

    return reservations


# -------------------- Reservation Logic --------------------

def reserve_car(cars, reservations, car_id, user_name, start_str, end_str):
    """
    Same as your original function, but now saves to JSON.
    """
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    if end_date < start_date:
        return None

    selected_car = None
    for c in cars:
        if c.getid() == car_id:
            selected_car = c
            break

    if selected_car is None:
        return None

    if not selected_car.is_avalible():
        return None

    days = (end_date - start_date).days + 1
    total_price = days * selected_car.getrent()

    new_id = len(reservations) + 1
    reservation = Reservation(new_id, user_name, selected_car, start_date, end_date, total_price)
    reservations.append(reservation)

    selected_car.avl = False  # simple rule

    # persist to file
    save_reservations(reservations)

    return reservation


# -------------------- History Helpers --------------------

def get_user_reservations(reservations, user_name):
    return [r for r in reservations if r.user_name == user_name]


def get_all_reservations(reservations):
    return list(reservations)
