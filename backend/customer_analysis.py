from collections import defaultdict
from copy import deepcopy

def analyze_customer_preferences(reservations):
    """
    -------------------------------------------------------
    Analyzes customer preferences based on completed rentals.
    It tracks frequency of car model names, car types (SUV, Truck, etc.),
    and fuel types (Gasoline, Electric, etc.) from the reservations.
    -------------------------------------------------------
    Parameters:
        reservations - List of Reservation objects (list) - assumes these
        represent completed rentals as per Sprint 3 goal.
    Returns:
    analysis - Dictionary containing the preference analysis:
        {
        'popular_models': {'Car Name A': 10, 'Car Name B': 5, ...},
        'popular_types': {'SUV': 12, 'Luxury': 8, ...},
        'popular_fuels': {'Gasoline': 15, 'Electric': 5, ...}
        } (dict)
    -------------------------------------------------------
    """
    # Use defaultdict to simplify counting
    model_counts = defaultdict(int)
    type_counts = defaultdict(int)
    fuel_counts = defaultdict(int)

    for res in reservations:
        # Access the car object linked to the reservation
        car = res.car
        
        # Count by Model Name
        model_name = car.getname()
        model_counts[model_name] += 1
        
        # Count by Car Type
        car_type = car.gettype()  # e.g., "SUV"
        type_counts[car_type] += 1
        
        # Count by Fuel Type
        fuel_type = car.getfuel()  # e.g., "Gasoline"
        fuel_counts[fuel_type] += 1
        
    analysis = {
        'popular_models': dict(model_counts),
        'popular_types': dict(type_counts),
        'popular_fuels': dict(fuel_counts)
    }

    return analysis

def display_preference_report(analysis):
    """
    -------------------------------------------------------
    Displays a formatted report of customer preferences.
    -------------------------------------------------------
    Parameters:
        analysis - Dictionary output from analyze_customer_preferences (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    print("==============================================")
    print("      CUSTOMER PREFERENCE ANALYSIS REPORT     ")
    print("==============================================")

    def print_section(title, data_dict):
        print(f"\n{title}")
        print("-" * len(title))
        if not data_dict:
            print("No data available yet.")
            return

        # Sort by count (highest first)
        sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_items:
            print(f"{name}: {count} rentals")

    print_section("Most Popular Models", analysis.get('popular_models', {}))
    print_section("Most Popular Car Types", analysis.get('popular_types', {}))
    print_section("Most Popular Fuel Types", analysis.get('popular_fuels', {}))

    print("\n(Report based on current reservations in the system.)\n")