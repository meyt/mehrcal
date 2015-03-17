# -*- coding: utf-8 -*-

###
# Calendar's definition
# =====================
# reWrite from gahshomar calendar (author Amir Mohammadi <183.amir@gmail.com> )
###
from calendar import Calendar, monthrange
from khayyam import jalali_date
import datetime
import calendar
import khayyam as khayyam
import core.general as general

try:
    xrange
except NameError:
    xrange = range

def add_years(date, years):
    while True:
        try:
            return date.replace(year=date.year+years)
        except ValueError:
            date -= datetime.timedelta(days=1)


def date_to_georgian(date):
    if isinstance(date, khayyam.JalaliDate):
        return date.to_date()
    return date


def add_one_month(t):
    u"""Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month earlier.
    Note that the resultant day of the month might change if the following
    month has fewer days:
        >>> add_one_month(datetime.date(2010, 1, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_later = t + one_day
    while one_month_later.month == t.month:  # advance to start of next month
        one_month_later += one_day
    target_month = one_month_later.month
    while one_month_later.day < t.day:  # advance to appropriate day
        one_month_later += one_day
        if one_month_later.month != target_month:  # gone too far
            one_month_later -= one_day
            break
    return one_month_later


def subtract_one_month(t):
    u"""Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month later.
    Note that the resultant day of the month might change if the following
    month has fewer days:
        >>> subtract_one_month(datetime.date(2010, 3, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_earlier = t - one_day
    while one_month_earlier.month == t.month or one_month_earlier.day > t.day:
        one_month_earlier -= one_day
    return one_month_earlier


def add_months(date, months):
    u'''http://code.activestate.com/recipes/
    577274-subtract-or-add-a-month-to-a-datetimedate-or-datet/
    Note: months may be positive, or negative, but must be an integer.
    If favorEoM (favor End of Month) is true and input date is the last day
    of the month then return an offset date that also falls on the last day
    of the month.'''
    if months == 0:
        return date
    elif months > 0:
        for __ in xrange(months):
            date = add_one_month(date)
    else:
        for __ in xrange(abs(months)):
            date = subtract_one_month(date)
    return date



class MyCalendar():

    def get_first_day_month(self):
        first_day_of_month = self.date+datetime.timedelta(days=1-self.date.day)
        first_day_of_month = first_day_of_month.weekday()
        first_day_of_month = (first_day_of_month) % 7
        # print('first_day_of_month', first_day_of_month)
        return first_day_of_month

    
    def gen_grid_mat(self, RTL=False):
        # decide if it is going to be 6 rows or 5
        if self.get_first_day_month() + self.get_days_in_month() > 35:
            rows = 6
        else:
            rows = 5

        self.grid_mat = []  # 5 or 6 row, 7 column
        for __ in xrange(rows):
            row = []
            for __ in xrange(7):
                row.append([])
            self.grid_mat.append(row)
        delta = - (self.get_first_day_month() + self.date.day) + 1
        # print(delta)
        for j in xrange(rows):
            for i in xrange(7):
                if RTL:
                    delta_time = datetime.timedelta(days=6-i+j*7+delta)
                else:
                    delta_time = datetime.timedelta(days=i+j*7+delta)
                date = self.date+delta_time
                # if date.month == self.date.month:
                #     text = '<span fgcolor="black">{}</span>'
                # else:
                #     text = '<span fgcolor="gray">{}</span>'
                text = u'{}'
                d = date.strftime(u'%d')
                if d[0] == u'0' or d[0] == u'۰':
                    d = d[1:]
                self.grid_mat[j][i] = (date, text.format(d))



class PersianCalendar(MyCalendar):

    def __init__(self, date=None, *args, **kwargs):
        if date is None:
            date = khayyam.JalaliDate.today()
        date = self.get_date(date)
        self.date = date
        self.first_week_day_offset = 2


    def get_days_in_month(self):
        return self.date.days_in_month


    def get_date(self, date):
        date = khayyam.JalaliDate.from_date(date_to_georgian(date))
        return date


    def get_week_days(self):
        return [(u'ش', u'شنبه'), (u'۱ش', u'یک‌شنبه'),
                (u'۲ش', u'دو‌شنبه'), (u'۳ش', u'سه‌شنبه'),
                (u'۴ش', u'چهار‌شنبه'), (u'۵ش', u'پنج‌شنبه'),
                (u'آ', u'آدینه')]


    def get_months(self):
        return list(jalali_date.PERSIAN_MONTH_NAMES.values())


    def get_months_abbr(self):
        return list(jalali_date.PERSIAN_MONTH_ABBRS.values())


    def add_one_month(self):
        one_day = datetime.timedelta(days=1)
        one_month_later = self.date + one_day
        while one_month_later.month == self.date.month:  # advance to start of next month
            one_month_later += one_day
        target_month = one_month_later.month
        while one_month_later.day < self.date.day:  # advance to appropriate day
            one_month_later += one_day
            if one_month_later.month != target_month:  # gone too far
                one_month_later -= one_day
                break
        return one_month_later


    def subtract_one_month(self):
        import datetime
        one_day = datetime.timedelta(days=1)
        one_month_earlier = self.date - one_day
        while one_month_earlier.month == self.date.month or one_month_earlier.day > self.date.day:
            one_month_earlier -= one_day
        return one_month_earlier





class GregorianCalendar(MyCalendar):
    def __init__(self, date=None, *args, **kwargs):
        if date is None:
            date = datetime.date.today()
        self.date = self.get_date(date)
        self.first_week_day_offset = 0

    
    def get_days_in_month(self):
        return monthrange(self.date.year, self.date.month)[1]


    def get_date(self, date):
        return date_to_georgian(date)

    
    def get_week_days(self):
        return [(u'Mon', u'Monday'), (u'Tue', u'Tuesday'),
                (u'Wed', u'Wednesday'), (u'Thu', u'Thursday'),
                (u'Fri', u'Friday'), (u'Sat', u'Saturday'),
                (u'Sun', u'Sunday')]

    
    def get_months(self):
        return list(calendar.month_name[1:])


    def get_months_abbr(self):
        return list(calendar.month_abbr[1:])

