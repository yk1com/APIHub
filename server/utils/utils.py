import datetime

def getNow() :
    # Get current date and time
    current_datetime = datetime.datetime.now()

    # Extract year, month, and day
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day

    # Extract hour, minute, and second
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    # Print the results in the format year-month-day hour:minutes:seconds
    return f"{year}-{month:02d}-{day:02d}-{hour:02d}-{minute:02d}-{second:02d}"