def get_capture_data(date):
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")

    return f'{day}/{month}/{year}'