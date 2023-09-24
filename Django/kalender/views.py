import calendar
from datetime import date, time, datetime, timedelta
from typing import Any, Dict
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect,  HttpResponse
from django.urls import reverse, re_path
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import  ListView, TemplateView, FormView
from django.contrib import messages
from django.db.models import Q
from .forms import WeekReservationForm, DayReservationForm
from .models import Event, ClosedDay, Calendar, ClosedTimeWindow, Rule
from Terminplaner.decorator import authenticated_user, no_further_details


class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "kalender/homepage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['calendars'] = Calendar.objects.all()
        rules = Rule.objects.all()
        context['rules'] = rules

        return context


############################################################################
# Day

@method_decorator(authenticated_user(), name='dispatch')
class DayCalendarPage(FormView):
    form_class = DayReservationForm
    template_name = "kalender/daycalendar.html"

    #Aktuell noch hart codierter Pfad
    def get_success_url(self):
        pk = self.kwargs['pk']
        selected_date = self.request.GET.get('selectedDate')
        success_url = f'/calendar/{pk}/'
        if selected_date:
            success_url += f'?selectedDate={selected_date}'
        return success_url

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        selected_date = self.request.GET.get('selectedDate')
        print(selected_date)
        initial_data = {}
        if selected_date:
            initial_data['event_date'] = selected_date
        else:
            today = datetime.now()
            initial_data['event_date'] = today.strftime('%Y-%m-%d')
        initial.update(initial_data)
        return initial

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['calendars'] = Calendar.objects.all()
        
        # Datetime's für die Navigation im Kalender erstellen
        str_query_date = self.request.GET.get('selectedDate', None)

        if str_query_date:
            try:
                query_date = datetime.strptime(str_query_date, '%Y-%m-%d').date()
            except ValueError:
                query_date = None
        else:
            query_date = datetime.today()
        

        prev_date = query_date - timedelta(days=1) 
        next_date = query_date + timedelta(days=1) 
        
        
        context['selected_date'] = date(query_date.year, query_date.month, query_date.day)
        context['previous_date'] = prev_date.strftime('%Y-%m-%d')
        context['next_date'] = next_date.strftime('%Y-%m-%d')

        # Kalender-Info (Zeiten und Buchungen des angezeigten Tages erstellen)
        current_calendar = Calendar.objects.get(id=self.kwargs['pk'])
        context["current_calendar"] = current_calendar

        occupancy_colors = current_calendar.color_json
        closed_color = occupancy_colors[str(len(occupancy_colors)-1)]

        start_of_day = timezone.make_aware(datetime(query_date.year, query_date.month, query_date.day, current_calendar.open_from.hour, current_calendar.open_from.minute, 0))
        end_of_day = timezone.make_aware(datetime(query_date.year, query_date.month, query_date.day, current_calendar.open_till.hour, current_calendar.open_till.minute, 0))

        interval = []  
        current_time = start_of_day
        while current_time < end_of_day:
            interval.append(current_time)
            current_time += timedelta(minutes=15)
        
        query_blocked_date = date(year=query_date.year, month=query_date.month, day=query_date.day)
        closed_day = ClosedDay.objects.filter(datum=query_blocked_date, calendar=current_calendar)

        if closed_day:
            day_info = []
            for index, item in enumerate(interval):
                day_info.append({
                    "interval" : item,
                    "number_of_Events" : 0,
                    "occupancy_colors" : closed_color,
                })

            context['calendar_infos'] = day_info
            context['closing_reason'] = closed_day[0].reason
            
        else:
            
            closed_time_window_queryset = ClosedTimeWindow.objects.filter(calendar=current_calendar,
                                                    start_time__year = query_date.year,
                                                    start_time__month = query_date.month,
                                                    start_time__day = query_date.day)
            
            events_queryset = Event.objects.filter(calendar=current_calendar,
                                                    start_time__year = query_date.year,
                                                    start_time__month = query_date.month,
                                                    start_time__day = query_date.day)
            
            day_info = []
            for index, item in enumerate(interval):

                start = item 
                end = item + timedelta(minutes=14)

                st_starts_whitin = Q(start_time__gte=start, start_time__lte=end)
                et_ends_whitin = Q(end_time__gte=start, end_time__lte=end)
                encapsulate = Q(start_time__lte=start, end_time__gte=end)

                closed_time_window = closed_time_window_queryset.filter(st_starts_whitin | et_ends_whitin | encapsulate)

                if bool(closed_time_window):

                    day_info.append({
                        "interval" : item,
                        "occupancy_colors" : closed_color,
                        "closed_time_window_reason" : closed_time_window[0].reason
                    })

                else:
                    
                    number_of_Events = events_queryset.filter(st_starts_whitin | et_ends_whitin | encapsulate).count()

                    day_info.append({
                        "interval" : item,
                        "number_of_Events" : number_of_Events,
                        "occupancy_colors" : occupancy_colors[str(number_of_Events)]
                    })

            context['calendar_infos'] = day_info
        
        return context


    def form_valid(self, form: Any) -> HttpResponse:
        data = form.cleaned_data
        current_calendar = Calendar.objects.get(id=self.kwargs['pk'])

        open_from = current_calendar.open_from
        open_till = current_calendar.open_till


        if data['event_time_start'] >= open_from and data['event_time_start'] <= open_till:
            start_time = timezone.make_aware(data['event_time_start']) 
            end_time = timezone.make_aware(data['event_time_end'])

            event_start_Tsp = datetime.combine(data['event_date'], start_time)
            event_end_Tsp = datetime.combine(data['event_date'], end_time)

            if start_time >= end_time or data['event_date'] < date.today() :
                messages.add_message(self.request, messages.WARNING, 'Bitte gib dir Mühe bei der Eingabe')
            else:
                user = self.request.user
                calendar = current_calendar
                use_type = data['use_type']
                new_event_data = {
                    'start_time' : event_start_Tsp,
                    'end_time' : event_end_Tsp,
                    'user' : user,
                    'calendar' : calendar,
                    'use_type' : use_type
                }

                if events_of_user_check(new_event_data):
                    messages.add_message(self.request, messages.WARNING, 'Du hast zu dieser Zeit bereits eine Reservation')
                elif vacancy_check(new_event_data, current_calendar):
                    messages.add_message(self.request, messages.WARNING, 'Keine weiteren Reservationen mehr möglich')
                elif closed_time_window_check(new_event_data, current_calendar):
                    messages.add_message(self.request, messages.WARNING, 'Zu dieser Zeit kann keine Reservation gemacht werden')
                elif closed_day_check(new_event_data, current_calendar):
                    messages.add_message(self.request, messages.WARNING, 'An diesem Tag kann keine Reservation gemacht werden')
                else: 
                    new_event = Event(**new_event_data)
                    new_event.save()  
                    messages.add_message(self.request, messages.SUCCESS, 'Zeitfenster reserviert')
        else:
            messages.add_message(self.request, messages.WARNING, 'Zu dieser Zeit kann keine Reservation gemacht werden')

        return super().form_valid(form)

def events_of_user_check(event_data):

    start = event_data['start_time']
    end = event_data['end_time']

    user_events = Event.objects.filter(user__username = event_data['user'].username,
                                    calendar = event_data['calendar'],
                                    start_time__year = event_data['start_time'].year,
                                    start_time__month = event_data['start_time'].month,
                                    start_time__day = event_data['start_time'].day)
    
    st_starts_whitin = Q(start_time__gte=start, start_time__lte=end)
    et_ends_whitin = Q(end_time__gte=start, end_time__lte=end)
    swallows = Q(start_time__gte=start, end_time__lte=end)
    encapsulate = Q(start_time__lte=start, end_time__gte=end)

    return bool(user_events.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows))

def vacancy_check (event_data, current_calendar):   

    start = event_data['start_time']
    end = event_data['end_time']

    events = Event.objects.filter(calendar = current_calendar,
                                    start_time__year = event_data['start_time'].year,
                                    start_time__month = event_data['start_time'].month,
                                    start_time__day = event_data['start_time'].day) 
       
    st_starts_whitin = Q(start_time__gte=start, start_time__lte=end)
    et_ends_whitin = Q(end_time__gte=start, end_time__lte=end)
    swallows = Q(start_time__gte=start, end_time__lte=end)
    encapsulate = Q(start_time__lte=start, end_time__gte=end)

    events_check = events.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows)

    cant_do_reservation = bool(events_check and events_check.count() >= current_calendar.persons_per_slot)

    if cant_do_reservation:
        deeper_check = False
        current_time = start
        while current_time < end:
            
            end_Intervall = current_time + timedelta(minutes=15) 
            
            st_starts_whitin = Q(start_time__gte=current_time, start_time__lte=end_Intervall)
            et_ends_whitin = Q(end_time__gte=current_time, end_time__lte=end_Intervall)
            swallows = Q(start_time__gte=current_time, end_time__lte=end_Intervall)
            encapsulate = Q(start_time__lte=current_time, end_time__gte=end_Intervall)
            deeper_check = events_check.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows).count() >= current_calendar.persons_per_slot
            if deeper_check:
                break
            current_time = end_Intervall
        return deeper_check
    else: 
        return cant_do_reservation


def closed_day_check(event_data, current_calendar):
    
    query_date = date(year=event_data['start_time'].year, month=event_data['start_time'].month, day=event_data['start_time'].day)
    closed_day = ClosedDay.objects.filter(datum=query_date, calendar=current_calendar)
    
    return bool(closed_day)


def closed_time_window_check(event_data, current_calendar):

    start = event_data['start_time']
    end = event_data['end_time']

    closed_time_windows = ClosedTimeWindow.objects.filter(calendar = current_calendar,
                                start_time__year = event_data['start_time'].year,
                                start_time__month = event_data['start_time'].month,
                                start_time__day = event_data['start_time'].day) 
    
    st_starts_whitin = Q(start_time__gte=start, start_time__lte=end)
    et_ends_whitin = Q(end_time__gte=start, end_time__lte=end)
    swallows = Q(start_time__gte=start, end_time__lte=end)
    encapsulate = Q(start_time__lte=start, end_time__gte=end)

    return bool(closed_time_windows.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows))



############################################################################
# WEEK .2

@method_decorator(authenticated_user(), name='dispatch')
class WeekCalendar2Page(TemplateView):
    http_method_names = ["get"]
    template_name = "kalender/weekcalendar2.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            self.request = request
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['calendars'] = Calendar.objects.all()

        # Datetime's für die Navigation im Kalender erstellen
        str_query_date = self.request.GET.get('selectedDate', None)

        if str_query_date:
            try:
                query_date = datetime.strptime(str_query_date, '%Y-%m-%d').date()
            except ValueError:
                query_date = None
        else:
            query_date = datetime.today()
        

        prev_date = query_date - timedelta(days=7) 
        next_date = query_date + timedelta(days=7) 
        
        context['selected_date'] = date(query_date.year, query_date.month, query_date.day)
        context['previous_date'] = prev_date.strftime('%Y-%m-%d')
        context['next_date'] = next_date.strftime('%Y-%m-%d')

        # Kalender-Info (Zeiten und Buchungen des angezeigten Tages erstellen)
        current_calendar = Calendar.objects.get(id=self.kwargs['pk'])
        context["current_calendar"] = current_calendar

        #Ggf. In Calendar Model einbauen, so dass jeder kalender andere farben anhand seiner anzahl buchungen haben kann
        occupancy_colors = current_calendar.color_json
        closed_color = occupancy_colors[str(len(occupancy_colors)-1)]

        #Stunden des Kalenders berechnen
        start_of_day = timezone.make_aware(datetime(query_date.year, query_date.month, query_date.day, current_calendar.open_from.hour, current_calendar.open_from.minute, 0))
        end_of_day = timezone.make_aware(datetime(query_date.year, query_date.month, query_date.day, current_calendar.open_till.hour, current_calendar.open_till.minute, 0))

        interval = []  
        current_time = start_of_day
        while current_time < end_of_day:
            interval.append(current_time)
            current_time += timedelta(hours=1)
        
        #Wochentage berechnen
        theDate = date(query_date.year, query_date.month, query_date.day)
        weekday = theDate.weekday()
        start_delta = timedelta(days=weekday)
        start_of_week = theDate - start_delta
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        
        #Wochentage mit closed_day , closed time windows und Events belegen
        week_info = {}
        for weekday in week_dates:
            day_info = []
            closing_reason = ''
            closed_day = ClosedDay.objects.filter(datum=weekday, calendar=current_calendar)
            if closed_day:
                for index, item in enumerate(interval):
                    day_info.append({
                        "interval" : item,
                        "number_of_Events" : 0,
                        "occupancy_colors" : closed_color,
                    })
                closing_reason = closed_day[0].reason 
            else:
                
                closed_time_window_queryset = ClosedTimeWindow.objects.filter(calendar=current_calendar,
                                        start_time__year = weekday.year,
                                        start_time__month = weekday.month,
                                        start_time__day = weekday.day)

                events_queryset = Event.objects.filter(calendar=current_calendar,
                                                        start_time__year = weekday.year,
                                                        start_time__month = weekday.month,
                                                        start_time__day = weekday.day)
                
                for index, item in enumerate(interval):
                    
                    start = timezone.make_aware(datetime(weekday.year,weekday.month,weekday.day,item.hour,item.minute))
                    end = timezone.make_aware(datetime(weekday.year,weekday.month,weekday.day,item.hour,item.minute)) + timedelta(minutes=59)
                    
                    st_starts_whitin = Q(start_time__gte=start, start_time__lte=end)
                    et_ends_whitin = Q(end_time__gte=start, end_time__lte=end)
                    swallows = Q(start_time__gte=start, end_time__lte=end)
                    encapsulate = Q(start_time__lte=start, end_time__gte=end)

                    closed_time_window = closed_time_window_queryset.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows)

                    if bool(closed_time_window):
                        
                        day_info.append({
                            "interval" : item,
                            "occupancy_colors" : closed_color,
                            "closed_time_window_reason" : closed_time_window[0].reason
                        })

                    else:

                        number_of_Events = events_queryset.filter(st_starts_whitin | et_ends_whitin | encapsulate |swallows).count()

                        if(number_of_Events > (len(occupancy_colors)-1)):
                            number_of_Events = len(occupancy_colors)-1

                        day_info.append({
                            "interval" : item,
                            "number_of_Events" : number_of_Events,
                            "occupancy_colors" : occupancy_colors[str(number_of_Events)]
                        })
            
            week_info[weekday.weekday()] = {
                "date": weekday,
                "day_infos" : day_info,
                "closing_reason": closing_reason
            }
        context['calendar_infos'] = week_info
           
        return context
    

##########################################################################
# HourDeteails

@method_decorator(no_further_details(), name='dispatch')
class OccupancyDetailPage(TemplateView):
    http_method_names = ["get"]
    template_name = "kalender/hourdetail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['calendars'] = Calendar.objects.all()

        current_calendar = Calendar.objects.get(id=self.kwargs['pk'])
        context["current_calendar"] = current_calendar

        str_date4details = self.request.GET.get('date', None)
        str_hour4details = self.request.GET.get('time', None)

        datetime4details_start = timezone.make_aware(datetime.strptime(str_date4details, "%Y-%m-%d")+timedelta(hours=int(str_hour4details)))
        datetime4details_end = datetime4details_start + timedelta(minutes=59)
        
        st_starts_whitin = Q(calendar=current_calendar,start_time__gte=datetime4details_start, start_time__lte=datetime4details_end)
        et_ends_whitin = Q(calendar=current_calendar,end_time__gte=datetime4details_start, end_time__lte=datetime4details_end)
        swallows = Q(calendar=current_calendar,start_time__gte=datetime4details_start, end_time__lte=datetime4details_end)
        encapsulate = Q(calendar=current_calendar,start_time__lte=datetime4details_start, end_time__gte=datetime4details_end)

        closed_day = ClosedDay.objects.filter(datum=datetime4details_start.date(), calendar=current_calendar)

        if bool(closed_day):
            context['closing_reason'] = closed_day[0].reason

        closed_time_windows = ClosedTimeWindow.objects.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows)
        
        events = Event.objects.filter(st_starts_whitin | et_ends_whitin | encapsulate | swallows)
        
        context['chosen_hour_start'] = datetime4details_start
        context['chosen_hour_end'] = datetime4details_end
        context['reservations'] = events
        context['closed_time_windows'] = closed_time_windows
        

        return context
    
###########################################################################
# Login

class LoginView(FormView):
    template_name = "registration/login.html"










