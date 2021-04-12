from calendar import HTMLCalendar
from accounts.models import MyUser
from .models import CalendarToDo

#日付の予定詳細
def get_todays_datail(request,date):
    try:
        data = CalendarToDo.objects.filter(username=request.user,date=date)
        details = []
        for d in data:
            date_sche = {'title':d.title,'start_time':d.start_time,'end_time':d.end_time,'date':d.date,'done':d.done,'discription':d.discription,'id':d.id}
            details.append(date_sche)
        return details
    except ValueError:
        details = []
        return details

#HTMLカレンダーを表示するクラス
class MyCalendar(HTMLCalendar):
    from .models import CalendarToDo
    from datetime import date

    today = date.today()
    def __init__(self,request,year = today.year,month = today.month, day=today.day,firstweekday=6):
        self.request=request
        self._year = year
        self._month = month
        self._day = day
        self.firstweekday = firstweekday
        self.japaneseWeek = ["月","火","水","木","金","土","日"]
    
    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr class="week_header" bgcolor="#1f253d">{}</tr>'.format(s)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '{}年 {}月'.format(theyear, themonth)
        else:
            s = '{}月'.format(themonth)
        return '<th colspan="3" class="{}">{}</th>'.format(
            self.cssclass_month_head, s)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th class="{}">{}</th>'.format(
            self.cssclasses_weekday_head[day], self.japaneseWeek[day])


    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        from .models import CalendarToDo
        from datetime import date
        try:
            events = CalendarToDo.objects.filter(username=self.request.user,date=date(self._year,self._month,day).isoformat())
        except ValueError:
            events = "failed"
            pass
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            today = date.today()
            if day==self._day and self._month==today.month:
                strs = '<td class="{} today active" onclick="onclickTd(this,{},{},{});"><span class="day">{}</span>'.format(self.cssclasses[weekday],self._year,self._month,day,day)
            else:
                strs = '<td class="{}" onclick="onclickTd(this,{},{},{});"><span class="day">{}</span>'.format(self.cssclasses[weekday],self._year,self._month,day,day)
            strs += '<ul>'
            for obj in events:
                hour = str(obj.start_time.hour)
                minute = str(obj.start_time.minute)
                start_time = '{}:{}'.format(hour.zfill(2),minute.zfill(2))
                if obj.done:
                    strs += '<li class="event_title"><s>{}<span class="strat_time">{}~</span></s></li>'.format(obj.title,start_time)
                else:
                    strs += '<li class="event_title">{}<span class="strat_time">{}~</span></li>'.format(obj.title,start_time)
            strs += '</ul></td>'
            return strs

    def formatmonth(self,withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="{}">'.format(
            self.cssclass_month))
        a('\n')
        a('<thead><tr class="t-title"><th colspan="2"><button id="premonth" class="btn" onclick="preClick()"></button></th>{}<th colspan="2"><button id="nextmonth" class="btn" onclick="nextClick()"></button></th></tr>'.format(
            self.formatmonthname(self._year, self._month, withyear=withyear)))
        a('\n')
        a(self.formatweekheader())
        a('</thead>')
        a('\n')
        for week in self.monthdays2calendar(self._year, self._month):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)