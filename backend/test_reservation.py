# -------------------------------------------------------
# test_rental_history.py
# -------------------------------------------------------
# Tests the persistent reservation system using the REAL
# reservations.json file.
#
# It checks:
#   - loading existing reservations
#   - creating a new reservation
#   - user-specific history
#   - "admin" all-reservations view
#
# WARNING: this will actually add reservations to your
# real reservations.json file.
# -------------------------------------------------------

from datetime import date
from car import Car
from reservation import (
    load_reservations,
    reserve_car,
    get_user_reservations,
    get_all_reservations,
)


def build_cars():
    """
    Builds the same car list used in main.py.
    Make sure this matches your real main.py car list.
    """
    cars = [
        Car(1, 0, 0, 5, 80.0,  True, 2022, "Toyota RAV4",    101),  # SUV, Gasoline
        Car(2, 1, 1, 2, 95.5,  False,2018, "Ford F-150",     102),  # Truck, Dieseal, unavailable
        Car(3, 3, 2, 4, 150.0, True, 2023, "Tesla Model S",  103),  # Luxury, Electric
        Car(4, 0, 0, 5, 55.0,  True, 2020, "Toyota Corolla", 104),  # SUV, Gasoline
        Car(5, 2, 0, 4, 45.0,  True, 2021, "Honda Fit",      105),  # Mid size, Gasoline
    ]
    return cars


def main():
    print("=== Rental History Persistent Test ===\n")

    # ----------------- Step 1: load existing data -----------------
    cars = build_cars()
    reservations = load_reservations(cars)

    print(f"Existing reservations loaded: {len(reservations)}")
    if reservations:
        print("Current reservations summary:")
        for r in reservations:
            print(
                f"  Res {r.res_id}: user={r.user_name}, car={r.car.getname()}, "
                f"dates={r.start_date}→{r.end_date}, total=${r.total_price:.2f}"
            )
    else:
        print("  (No reservations yet.)")
    print("-" * 40)

    # ----------------- Step 2: find an available car -----------------
    available_cars = [c for c in cars if c.is_avalible()]
    if not available_cars:
        print("⚠ No available cars to test reservation creation.")
        print("   Test will skip the 'create reservation' part.\n")
    else:
        test_user = "test_user_history"
        test_car = available_cars[0]

        print(f"Using car ID {test_car.getid()} ({test_car.getname()}) for test reservation.")
        # choose some simple test dates
        start_str = "2025-11-20"
        end_str = "2025-11-22"

        new_res = reserve_car(
            cars=cars,
            reservations=reservations,
            car_id=test_car.getid(),
            username=test_user,
            start_str=start_str,
            end_str=end_str,
        )

        if new_res is None:
            print("❌ Failed to create test reservation (reserve_car returned None).")
        else:
            print("✅ Test reservation created successfully:")
            print(
                f"  Res {new_res.res_id}: user={new_res.user_name}, car={new_res.car.getname()}, "
                f"dates={new_res.start_date}→{new_res.end_date}, total=${new_res.total_price:.2f}"
            )
            print(f"  Car now available? {new_res.car.is_avalible()}")
    print("-" * 40)

    # ----------------- Step 3: reload to ensure persistence -----------------
    cars2 = build_cars()
    reservations2 = load_reservations(cars2)
    print(f"Reservations after reload: {len(reservations2)}")

    # ----------------- Step 4: user-specific history -----------------
    print("\n=== User-specific history check ===")
    user_hist = get_user_reservations(reservations2, "test_user_history")
    print(f"Reservations for 'test_user_history': {len(user_hist)}")
    for r in user_hist:
        print(
            f"  Res {r.res_id}: car={r.car.getname()}, dates={r.start_date}→{r.end_date}, "
            f"total=${r.total_price:.2f}"
        )

    # ----------------- Step 5: admin-style all reservations -----------------
    print("\n=== Admin all-reservations view ===")
    all_hist = get_all_reservations(reservations2)
    print(f"Total reservations in system: {len(all_hist)}")
    for r in all_hist:
        print(
            f"  Res {r.res_id}: user={r.user_name}, car={r.car.getname()}, "
            f"dates={r.start_date}→{r.end_date}, total=${r.total_price:.2f}"
        )

    print("\n=== Test complete ===")


if __name__ == "__main__":
    main()
