# -------------------------------------------------------
# test_rental_history.py
# -------------------------------------------------------
# Simple tests for:
#   - reserve_car
#   - get_user_reservations
#   - get_all_reservations
# -------------------------------------------------------

from car import Car
from reservation import reserve_car, get_user_reservations, get_all_reservations


def main():
    cars = [
        Car(1, 0, 0, 5, 80.0,  True, 2022, "Toyota RAV4",    101),
        Car(2, 3, 2, 4, 150.0, True, 2023, "Tesla Model S",  102),
        Car(3, 2, 0, 4, 45.0,  True, 2021, "Honda Fit",      103),
    ]

    reservations = []  # this will be filled as we reserve cars

    # ----------------- Test 1: empty history -----------------
    print("=== Test 1: Empty history ===")
    alice_hist = get_user_reservations(reservations, "alice")
    all_hist = get_all_reservations(reservations)

    if len(alice_hist) == 0 and len(all_hist) == 0:
        print("✅ Test 1 PASSED: no reservations initially.")
    else:
        print("❌ Test 1 FAILED: expected empty histories at start.")
    print("-" * 40)

    # ----------------- Test 2: create reservations -----------------
    print("=== Test 2: Create reservations and check history ===")

    res1 = reserve_car(
        cars=cars,
        reservations=reservations,
        car_id=1,                      # Toyota RAV4
        user_name="alice",
        start_str="2025-11-20",
        end_str="2025-11-22",
    )

    res2 = reserve_car(
        cars=cars,
        reservations=reservations,
        car_id=2,                      # Tesla Model S
        user_name="bob",
        start_str="2025-12-01",
        end_str="2025-12-03",
    )

    if res1 is None or res2 is None:
        print("❌ Test 2 FAILED: expected two successful reservations.")
    elif len(reservations) != 2:
        print("❌ Test 2 FAILED: reservations list size is not 2.")
    else:
        print("✅ Test 2 PASSED: two reservations created.")

    # check availability of reserved cars
    print(f"Car 1 available? {cars[0].is_avalible()}")
    print(f"Car 2 available? {cars[1].is_avalible()}")
    print("-" * 40)

    # ----------------- Test 3: user-specific history -----------------
    print("=== Test 3: User-specific histories ===")

    alice_hist = get_user_reservations(reservations, "alice")
    bob_hist = get_user_reservations(reservations, "bob")
    charlie_hist = get_user_reservations(reservations, "charlie")  # no reservations

    ok = True
    if len(alice_hist) != 1 or alice_hist[0].user_name != "alice":
        print("❌ Test 3 FAILED: alice history incorrect.")
        ok = False
    if len(bob_hist) != 1 or bob_hist[0].user_name != "bob":
        print("❌ Test 3 FAILED: bob history incorrect.")
        ok = False
    if len(charlie_hist) != 0:
        print("❌ Test 3 FAILED: charlie should have no reservations.")
        ok = False

    if ok:
        print("✅ Test 3 PASSED: user histories are correct.")
    print("-" * 40)

    # ----------------- Test 4: admin-style 'all reservations' -----------------
    print("=== Test 4: All reservations (admin view) ===")

    all_hist = get_all_reservations(reservations)
    if len(all_hist) == 2:
        print("✅ Test 4 PASSED: admin sees all reservations.")
    else:
        print("❌ Test 4 FAILED: admin history size incorrect.")

    print("\n--- All reservations summary ---")
    for r in all_hist:
        print(
            f"Res {r.res_id}: user={r.user_name}, car={r.car.getname()}, "
            f"dates={r.start_date}→{r.end_date}, total=${r.total_price:.2f}"
        )
    print("--------------------------------")


if __name__ == "__main__":
    main()
