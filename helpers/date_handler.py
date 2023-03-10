from datetime import date, datetime, timedelta


def date_range(pull_type):
    now = datetime.today()
    if pull_type.upper() == "WEEKLY":
        day = now.strftime("%d/%m/%Y")
        dt = datetime.strptime(day, "%d/%m/%Y")
        start = dt - timedelta(days=dt.isoweekday() + 7)
        end = start + timedelta(days=6)
    elif pull_type.upper() == "MONTHLY":
        now = now.replace(day=1)
        end = now - timedelta(days=1)
        start = end.replace(day=1)
    return str(start.strftime("%Y-%m-%d")), str(end.strftime("%Y-%m-%d"))


if __name__ == '__main__':
    start, end = date_range("monthly")
    print(start)
    print(end)
