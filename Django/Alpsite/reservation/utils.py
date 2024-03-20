from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from django.db.models import Q
from .models import Reservation
from django.contrib.auth.models import User
 

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	def formatday(self, day, reservations):

		bg_color = ""
		
		if day != int(0):
			day_date = date(year=self.year, month=self.month, day=day)

			begin_of_reservation =  reservations.filter(from_date=day_date).values()
			if begin_of_reservation:
				user = User.objects.get(id=begin_of_reservation[0]['user_id'])

			is_part_of_reservation = Q(from_date__lte=day_date, to_date__gte=day_date)
			reserved = reservations.filter(is_part_of_reservation)
			
			if bool(reserved.filter(approved=False).values()):
				bg_color = "request"
			elif bool(reserved.filter(approved=True).values()):
				bg_color = "reservation"
			
		if day != 0:
			if bool(begin_of_reservation):
				return f"<td class='{bg_color}'><span class='date'>{day}</span><br><span class='user'>{user.username[0:8]}</span></td>"
			else:
				return f"<td class='{bg_color}'><span class='date'>{day}</span><br><span style='opacity: 0.0;'>leer</span></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, reservations):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, reservations)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	def formatmonth(self, withyear=True):

		starts_whitin = Q(from_date__year=self.year, from_date__month=self.month)
		ends_whitin = Q(to_date__year=self.year, to_date__month=self.month)

		reservations = Reservation.objects.filter(starts_whitin | ends_whitin)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, reservations)}\n'
		cal += f'</table>'
		
		return cal

### Delete Reservation ###	

def delete_reservation(reservationID):
    try:
        reservation = Reservation.objects.get(id=reservationID)
        reservation.delete()  
        return True 
    except (Reservation.DoesNotExist):
        return False  


