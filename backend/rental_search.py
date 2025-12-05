# -------------------------------------------------------
# Rental Car Search - Backend
# -------------------------------------------------------
# Provides full search/filtering over a list of Car objects.
# Filters include: type, fuel, year range, seat count,
# price range, availability, and name matching.
# -------------------------------------------------------

def search_cars(
    cars,
    type=None,
    fuel=None,
    year_min=None,
    year_max=None,
    min_seats=None,
    price_min=None,
    price_max=None,
    only_available=False,
    name_contains=None
):
    results = []

    for c in cars:
        # Type filter
        if type is not None and c.gettype().lower() != type.lower():
            continue

        # Fuel filter
        if fuel is not None and c.getfuel().lower() != fuel.lower():
            continue

        # Year range filter
        if year_min is not None and c.getyear() < year_min:
            continue
        if year_max is not None and c.getyear() > year_max:
            continue

        # Seats filter
        if min_seats is not None and c.getpassengers() < min_seats:
            continue

        # Price range filter
        if price_min is not None and c.getrent() < price_min:
            continue
        if price_max is not None and c.getrent() > price_max:
            continue

        # Availability filter
        if only_available and not c.is_avalible():
            continue

        # Name search filter
        if name_contains is not None and name_contains.lower() not in c.getname().lower():
            continue

        # Append the REAL car object, not a deepcopy
        results.append(c)

    return results