# MehrCal
تقویم "مهر"

*ver0.3 dev*

a simple persian calendar application for linux 

یک تقویم ساده پارسی برای گنو/لینوکس

![MehrCal screenshot](https://raw.githubusercontent.com/meyt/mehrcal/master/mehrcal-screenshot.png)


### قابلیت ها
- نمایش تقویم میلادی و شمسی
- تنظیم رنگ روزهای تعطیل
- تنظیم چینش روز ها
- توسعه از طریق افزونه ها

### افزونه های پیش فرض

#### افزونه رویداد ها
رویداد های شمسی، میلادی و قمری بر اساس تقویم رسمی ایران

##### قابلیت ها
- علامت زدن روز های دارای رویداد
- افزودن روز های تعطیل بر اساس رویداد ها
- تنظیم نمایش رویداد ها بر روی تقویم
- نمایش رویداد ها با نگه داشتن ماوس tooltip

##### مشکلات فعلی 
- عدم هماهنگی رویداد های برخی از روزهای تقویم قمری به دلیل اختلاف طول ماه های قمری
- تنظیم ترجمه زبان جداگانه برای هر پلاگین
- چینش المنت ها بر اساس زبان فعلی

### پیش‌نیاز ها
- Python >= 2.7
- Gtk+ >= 3


### نصب
در توزیع های بر پایه دبیان:

    sudo apt-get install python-pip python-setuptools

در توضیع های برپایه ارچ:

    sudo pacman -S python-pip python-setuptools

برنامه را از حالت فشرده خارج کنید و به داخل فولدر با دستور

    cd 

برید و بعد دستور زیر رو اجرا کنید:

	sudo python ./setup.py install 

### بدون نصب
میتونید برنامه رو بدون نصب هم اجرا کنید.


### لینک های مربوط به این برنامه
Khayyam https://github.com/pylover/khayyam

StarCalendar https://github.com/ilius/starcal

Gahshomar https://github.com/183amir/gahshomar

Umalqurra https://github.com/tytkal/python-hijiri-ummalqura

