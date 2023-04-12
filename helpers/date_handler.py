"""Creates date range according to date argument"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def date_range(pull_type):
    now = datetime.today()
    date_range = list()

    if pull_type.lower() == "weekly":
        start, end = weekly(now)
        date_range = [[str(start.strftime("%Y-%m-%d")), str(end.strftime("%Y-%m-%d"))]]

    elif pull_type.lower() == "monthly":
        date_ref = now.replace(day=1)
        start, end = monthly(date_ref)
        date_range = [[str(start.strftime("%Y-%m-%d")), str(end.strftime("%Y-%m-%d"))]]

    elif pull_type.lower() == "monthly_history":
        date_ref = now.replace(day=1)
        for i in range(13):
            start, end = monthly(date_ref)
            date_range.append([str(start.strftime("%Y-%m-%d")), str(end.strftime("%Y-%m-%d"))])
            date_ref = start

    elif pull_type.lower() == "weekly_history":
        date_till = now.replace(day=1) - relativedelta(months=13)
        date_ref = now
        while date_ref > date_till:
            start, end = weekly(date_ref)
            date_range.append([str(start.strftime("%Y-%m-%d")), str(end.strftime("%Y-%m-%d"))])
            date_ref = end
    return date_range


def weekly(now):
    dt = now
    start = dt - timedelta(days=dt.isoweekday() + 7)
    end = start + timedelta(days=6)
    return start, end


def monthly(date_ref):
    end = date_ref - timedelta(days=1)
    start = end.replace(day=1)
    return start, end


if __name__ == '__main__':
    dates = date_range("weekly_history")
    # for date in dates:
    #     print(date[0])
    #     print(date[1])
