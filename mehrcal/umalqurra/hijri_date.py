# -*- coding: utf-8 -*-
'''
This is an API for Hijri Umalqurra Calendar,
it was developed  by khalid Al-hussayen 1436-3-15 2015-1-6.
The algrothem of converting hijri to  Gregorian is in hijri.py
This Api will give the ability to convert Gregorian To Hijri or Hijri to Gregorian with the day and month names in Hijri and Gregorian
You can query for the current day in both Hijri and Gregorian
'''
__author__ = 'Khalid'
from umalqurra.hijri import Umalqurra
from datetime import date
class HijriDate:
    #day in hijri
    day = -1
    #month in hijri
    month = -1
    #year in hijri
    year = -1
    day_gr = -1
    month_gr = -1
    year_gr = -1
    #day bane in arabic
    day_name = ''
    #month name in hijri
    month_name = ''
    month_dict = {
        1: u'محرم',
        2: u'صفر',
        3: u'ربيع الأول',
        4: u'ربيع الثاني',
        5: u'جمادي الأولى',
        6: u'جمادي الآخرة',
        7: u'رجب',
        8: u'شعبان',
        9: u'رمضان',
        10: u'شوال',
        11: u'ذو القعدة',
        12: u'ذو الحجة'
    }
    day_dict = {
        '6': u'السبت',
        '7': u'الاحد',
        '1': u'الاثنين',
        '2': u'الثلاثاء',
        '3': u'الاربعاء',
        '4': u'الخميس',
        '5': u'الجمعة'
    }
    month_name_gr = ''
    day_name_en = ''
    def __init__(self,year=None,month=None,day=None,gr=False):
        if year != None and month != None and day != None:
            if gr == False:
                self.set_date(year,month,day)
            else:
                self.set_date_from_gr(year,month,day)
    #Set dates if the date send by user is Gregorian
    def set_date_from_gr(self,year,month,day):
        um = Umalqurra()
        self.day_gr, self.month_gr, self.year_gr = day, month, year
        self.year, self.month, self.day = um.gegorean_to_hijri(year,month,day)
        self.month_name = self.month_dict[self.month]
        date_gr = date(year,month,day)
        self.day_name_en = date_gr.strftime("%u")
        self.day_name = self.day_dict[self.day_name_en]
        self.month_name_gr = date_gr.strftime("%B")
    #Set dates if date send by user is Hijri
    def set_date(self,year,month,day):
        um = Umalqurra()
        self.day, self.month, self.year = day, month, year
        self.month_name = self.month_dict[month]
        self.year_gr, self.month_gr, self.day_gr = um.hijri_to_gregorian(year,month,day)
        date_gr = date(int(self.year_gr),int(self.month_gr),int(self.day_gr))
        self.day_name_en = date_gr.strftime("%u")
        self.day_name = self.day_dict[self.day_name_en]
        self.month_name_gr = date_gr.strftime("%B")

    @classmethod
    def today(cls):
        today = date.today()
        hijri_date = HijriDate(today.year,today.month,today.day,True)
        return hijri_date