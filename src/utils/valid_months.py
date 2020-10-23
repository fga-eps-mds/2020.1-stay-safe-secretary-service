def get_all_valid_months(initial_period, final_period):
    """
    Return a list of all months in the given range.
    """
    valid_months = []

    initial_period = initial_period.split('/')
    initial_month = int(initial_period[0])
    initial_year = int(initial_period[1])

    final_period = final_period.split('/')
    final_month = int(final_period[0])
    final_year = int(final_period[1])

    while initial_year <= final_year:
        if initial_year < final_year:
            while initial_month <= 12:
                valid_months.append(f'{initial_month}/{initial_year}')
                initial_month += 1
            initial_month = 1
        elif initial_year == final_year:
            while initial_month <= final_month:
                valid_months.append(f'{initial_month}/{initial_year}')
                initial_month += 1
        initial_year += 1

    return valid_months
