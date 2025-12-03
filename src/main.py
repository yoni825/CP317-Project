# -------------------------------------------------------
# Car Rental System - Main
# -------------------------------------------------------
# - Handles login / registration
# - Lets user search for cars
# - Lets user reserve a car
# - Admin can view all reservations + customer preferences
# -------------------------------------------------------

from car import Car
from rental_search import search_cars        
from reservation import (
    reserve_car,
    save_reservations,
    load_reservations,
    get_user_reservations,
    get_all_reservations
)
from user_account import UserAccount, load_users, save_users

from customer_analysis import analyze_customer_preferences, display_preference_report


# Helper to define the Admin user
def is_admin_user(user):
    """Checks if the current user is the administrator."""
    return user is not None and user.username == "admin"


def main():
    # -----------------------------------------------
    # 1. User login / registration
    # -----------------------------------------------
    user_db = load_users()      # {username: UserAccount}
    current_user = None

    # Ensure there is an admin account
    # (Hard-coded for this project, fine for a school assignment.)
    if "admin" not in user_db:
        admin_pw_hashed = UserAccount.hash_password("admin123")
        user_db["admin"] = UserAccount("admin", admin_pw_hashed, email=None)
        save_users(user_db)

    print("==============================================")
    print("        Welcome to the Car Rental System      ")
    print("==============================================\n")

    choice = input("Login (L) or Register (R)? ").strip().lower()

    if choice == "l":
        # ----- LOGIN -----
        uname = input("Username: ").strip()
        pw = input("Password: ").strip()
        
        if uname in user_db and user_db[uname].verify_password(pw):
            current_user = user_db[uname]
            print(f"\n✅ Logged in as {current_user.username}\n")
        else:
            print("❌ Login failed. Exiting.")
            return

    elif choice == "r":
        # ----- REGISTER -----
        uname = input("Choose a username: ").strip()
        
        if uname in user_db:
            print("❌ Username already exists. Please try logging in instead.\n")
            return

        pw = input("Choose a password: ").strip()
        email = input("Email (optional): ").strip() or None

        hashed = UserAccount.hash_password(pw)
        user_db[uname] = UserAccount(uname, hashed, email)
        save_users(user_db)

        current_user = user_db[uname]
        print(f"\n✅ Account created! Logged in as {current_user.username}\n")

    else:
        # ----- INVALID CHOICE -----
        print("❌ Invalid choice. Exiting.")
        return


    # -----------------------------------------------
    # 2. Initial car inventory (sample data)
    # -----------------------------------------------
    cars = [
        Car(1, 0, 0, 5, 80.0,  True, 2022, "Toyota RAV4",    101),  # SUV, Gasoline
        Car(2, 1, 1, 2, 95.5,  True,2018, "Ford F-150",     102),  # Truck, Dieseal, unavailable
        Car(3, 3, 2, 4, 150.0, True, 2023, "Tesla Model S",  103),  # Luxury, Electric
        Car(4, 0, 0, 5, 55.0,  True, 2020, "Toyota Corolla", 104),  # SUV, Gasoline
        Car(5, 2, 0, 4, 45.0,  True, 2021, "Honda Fit",      105),  # Mid size, Gasoline
    ]

    reservations = load_reservations(cars)


    # -----------------------------------------------
    # 3. Main loop: search + history + admin features
    # -----------------------------------------------
    while True:
        is_admin = is_admin_user(current_user)

        print("Main Menu")
        print("1. Search for cars")
        print("2. Show ALL available cars")
        print("3. View my rental history")
        if is_admin:
            print("4. View ALL reservations (admin)")
            print("5. View customer preference analysis (admin)")
            print("6. Exit")
        else:
            print("4. Exit")

        menu_choice = input("Select an option: ").strip()

        # ------------------ Exit ------------------
        if (not is_admin and menu_choice == "4") or (is_admin and menu_choice == "6"):
            print("Goodbye!")
            break

        # ------------------ View my rental history ------------------
        if menu_choice == "3":
            my_res = get_user_reservations(reservations, current_user.username)
            if not my_res:
                print("\nYou have no past reservations yet.\n")
            else:
                print("\n=== Your Rental History ===\n")
                for r in my_res:
                    print(f"Reservation ID: {r.res_id}")
                    print(f"Car: {r.car.getname()} (ID: {r.car.getid()})")
                    print(f"Dates: {r.start_date} → {r.end_date}")
                    print(f"Total Price: ${r.total_price:.2f}")
                    print("-" * 40)
                print()
            continue

        # ------------------ Admin: view all reservations ------------------
        if is_admin and menu_choice == "4":
            all_res = get_all_reservations(reservations)
            if not all_res:
                print("\nNo reservations in the system yet.\n")
            else:
                print("\n=== ALL Reservations (Admin) ===\n")
                for r in all_res:
                    print(f"Reservation ID: {r.res_id}")
                    print(f"User: {r.user_name}")
                    print(f"Car: {r.car.getname()} (ID: {r.car.getid()})")
                    print(f"Dates: {r.start_date} → {r.end_date}")
                    print(f"Total Price: ${r.total_price:.2f}")
                    print("-" * 40)
                print()
            continue

        # ------------------ Admin: view customer preferences ------------------
        if is_admin and menu_choice == "5":
            if not reservations:
                print("\nNo reservations yet. Not enough data for preference analysis.\n")
            else:
                analysis = analyze_customer_preferences(reservations)
                display_preference_report(analysis)
            continue

        # ------------------ Show ALL available cars (no filters) ------------------
        if menu_choice == "2":
            available_cars = [c for c in cars if c.is_avalible()]

            if not available_cars:
                print("\n❌ No cars are currently available.\n")
                continue

            print("\n=== All Available Cars ===\n")
            for c in available_cars:
                print(f"Car ID: {c.getid()}")
                print(f"Name: {c.getname()}")
                print(f"Type: {c.gettype()}")
                print(f"Fuel: {c.getfuel()}")
                print(f"Year: {c.getyear()}")
                print(f"Seats: {c.getpassengers()}")
                print(f"Price per Day: ${c.getrent():.2f}")
                print(f"Available: {'Yes' if c.is_avalible() else 'No'}")
                print("-" * 40)

            # Let them reserve from this list
            reserve_choice = input("Would you like to reserve one of these cars? (y/n): ").strip().lower()
            if reserve_choice != "y":
                print()
                continue

            try:
                selected_id = int(input("Enter the Car ID you want to reserve: ").strip())
            except ValueError:
                print("Invalid Car ID.\n")
                continue

            start_str = input("Enter start date (YYYY-MM-DD): ").strip()
            end_str = input("Enter end date (YYYY-MM-DD): ").strip()

            res = reserve_car(
                cars=cars,
                reservations=reservations,
                car_id=selected_id,
                user_name=current_user.username,
                start_str=start_str,
                end_str=end_str
            )

            if res is None:
                print("\n❌ Reservation failed. Car may be unavailable, ID invalid, or dates invalid.\n")
            else:
                print("\n✅ Reservation successful!")
                print(f"Reservation ID: {res.res_id}")
                print(f"Customer: {res.user_name}")
                print(f"Car: {res.car.getname()} (ID: {res.car.getid()})")
                print(f"Dates: {res.start_date} → {res.end_date}")
                print(f"Total Price: ${res.total_price:.2f}")
                print(f"Car now available? {'Yes' if res.car.is_avalible() else 'No'}\n")

            continue

        # ------------------ Search with filters ------------------
        if menu_choice != "1":
            print("Invalid option.\n")
            continue

        print("\nEnter filters below (press Enter to skip any):\n")

        type_input = input("Car type (SUV, Truck, Mid size, Luxury): ").strip() or None
        fuel_input = input("Fuel type (Gasoline, Dieseal, Electric): ").strip() or None
        name_input = input("Search by car name: ").strip() or None

        try:
            year_min_str = input("Minimum year: ").strip()
            year_max_str = input("Maximum year: ").strip()
            price_min_str = input("Minimum price: ").strip()
            price_max_str = input("Maximum price: ").strip()
            min_seats_str = input("Minimum seats: ").strip()

            year_min = int(year_min_str) if year_min_str else None
            year_max = int(year_max_str) if year_max_str else None
            price_min = float(price_min_str) if price_min_str else None
            price_max = float(price_max_str) if price_max_str else None
            min_seats = int(min_seats_str) if min_seats_str else None
        except ValueError:
            print("Invalid number entered. Ignoring numeric filters.\n")
            year_min = year_max = price_min = price_max = min_seats = None

        only_available = input("Show only available cars? (y/n): ").strip().lower() == "y"

        print("\nSearching for cars...\n")

        results = search_cars(
            cars,
            type=type_input,
            fuel=fuel_input,
            year_min=year_min,
            year_max=year_max,
            min_seats=min_seats,
            price_min=price_min,
            price_max=price_max,
            only_available=only_available,
            name_contains=name_input
        )

        if not results:
            print("❌ No cars matched your search.\n")
            continue
        else:
            print("✅ Cars Found:\n")
            for c in results:
                print(f"Car ID: {c.getid()}")
                print(f"Name: {c.getname()}")
                print(f"Type: {c.gettype()}")
                print(f"Fuel: {c.getfuel()}")
                print(f"Year: {c.getyear()}")
                print(f"Seats: {c.getpassengers()}")
                print(f"Price per Day: ${c.getrent():.2f}")
                print(f"Available: {'Yes' if c.is_avalible() else 'No'}")
                print("-" * 40)

        reserve_choice = input("Would you like to reserve one of these cars? (y/n): ").strip().lower()
        if reserve_choice != "y":
            print()
            continue

        try:
            selected_id = int(input("Enter the Car ID you want to reserve: ").strip())
        except ValueError:
            print("Invalid Car ID.\n")
            continue

        start_str = input("Enter start date (YYYY-MM-DD): ").strip()
        end_str = input("Enter end date (YYYY-MM-DD): ").strip()

        res = reserve_car(
            cars=cars,
            reservations=reservations,
            car_id=selected_id,
            user_name=current_user.username,
            start_str=start_str,
            end_str=end_str
        )

        if res is None:
            print("\n❌ Reservation failed. Car may be unavailable, ID invalid, or dates invalid.\n")
        else:
            print("\n✅ Reservation successful!")
            print(f"Reservation ID: {res.res_id}")
            print(f"Customer: {res.user_name}")
            print(f"Car: {res.car.getname()} (ID: {res.car.getid()})")
            print(f"Dates: {res.start_date} → {res.end_date}")
            print(f"Total Price: ${res.total_price:.2f}")
            print(f"Car now available? {'Yes' if res.car.is_avalible() else 'No'}\n")


if __name__ == "__main__":
    main()
