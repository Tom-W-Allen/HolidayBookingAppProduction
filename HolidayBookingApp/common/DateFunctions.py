from datetime import datetime, timedelta, date, time


def get_valid_weekdays(start_date: datetime, end_date: datetime) -> "list[datetime]":
    difference = end_date - start_date

    valid_holidays = []

    checking_date = start_date

    for _ in range(0, difference.days + 1):
        if checking_date.isoweekday() not in [6, 7]:
            valid_holidays.append(checking_date)

        checking_date += timedelta(1)

    return valid_holidays


def find_overlapping_dates(start_date: datetime,
                           end_date: datetime,
                           comparison_start_date: datetime,
                           comparison_end_date: datetime) -> "list[datetime]":
    difference = end_date - start_date

    date_list = []
    date_to_add = start_date
    for _ in range(0, difference.days + 1):
        date_list.append(date_to_add)
        date_to_add += timedelta(1)

    return [x for x in date_list if comparison_start_date <= x <= comparison_end_date]

def format_database_date(value):
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    elif isinstance(value, str) and "-" in value:
        return datetime.strptime(value, "%Y-%m-%d")
    elif isinstance(value, str) and ":" in value:
        reformatted_time = [int(part) for part in value.split(":")]
        return time(reformatted_time[0], reformatted_time[1], reformatted_time[2])
    elif isinstance(value, time):
        return time(value.hour, value.minute, value.second)
    else:
        raise Exception("Unrecognised date format")