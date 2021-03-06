import datetime
import pendulum

from pytz import timezone

tz = timezone('Asia/Yekaterinburg')
one_day = datetime.timedelta(days=1)


def get_week(_date):
    day_idx = (_date.weekday()) % 7  # monday into 0, etc.
    monday = _date - datetime.timedelta(days=day_idx)
    _date = monday
    for n in range(7):
        yield _date
        _date += one_day
