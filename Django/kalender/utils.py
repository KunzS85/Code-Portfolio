from datetime import datetime, timedelta, date
from .models import Event, Calendar


def delete_event(calendarID, eventID):
    try:
        calendar = Calendar.objects.get(pk=calendarID) 
        event = Event.objects.get(calendar=calendar, pk=eventID)
        event.delete()  
        return True 
    except (Calendar.DoesNotExist, Event.DoesNotExist):
        return False  





