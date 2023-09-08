"""Creates date range according to date argument"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DateInit:
    def __init__(self):
        self.now = datetime.today()
        self.date_range = list()

    def week_range(self, date_ref):
        dt = date_ref
        start = dt - timedelta(days=dt.isoweekday() + 7)
        end = start + timedelta(days=6)
        return start, end

    def month_range(self, date_ref):
        end = date_ref - timedelta(days=1)
        start = end.replace(day=1)
        return start, end


class DateHandler(DateInit):
    def __init__(self, pull_type: str):
        super().__init__()
        self.pull_type = pull_type
        self.date_format = "%Y-%m-%d"
        method_list = {
            "weekly" : self.week_range,
            "monthly" : self.month_range,
        }
        if 'weekly' in self.pull_type.lower():
            self.choice = method_list.get('weekly')
        elif 'monthly' in self.pull_type.lower():
            self.choice = method_list.get('monthly')
    def regular_range(self):
        if self.pull_type.lower() == "weekly":
            start, end = self.choice(self.now)
            self.date_range = [start.strftime(self.date_format), end.strftime(self.date_format)]

        elif self.pull_type.lower() == "monthly":
            date_ref = self.now.replace(day=1)
            start, end = self.choice(date_ref)
            self.date_range = [start.strftime(self.date_format), end.strftime(self.date_format)]

        return self.date_range

    def historical_range(self):
        if self.pull_type.lower() == "monthly_history":
                date_ref = self.now.replace(day=1)
                for _ in range(13):
                    start, end = self.choice(date_ref)
                    self.date_range.append([start.strftime(self.date_format), end.strftime(self.date_format)])
                    date_ref = start

        elif self.pull_type.lower() == "weekly_history":
            date_till = self.now.replace(day=1) - relativedelta(months=13)
            date_ref = self.now
            while date_ref > date_till:
                start, end = self.choice(date_ref)
                self.date_range.append([start.strftime(self.date_format), end.strftime(self.date_format)])
                date_ref = end
        return self.date_range

