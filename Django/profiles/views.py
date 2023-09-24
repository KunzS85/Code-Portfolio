from typing import Any, Dict
from django.utils import timezone
from django.views.generic import DetailView, View
from django.contrib.auth.models import User
from django.contrib import messages
from kalender.models import Event, Calendar
from kalender.utils import delete_event
from django.utils.decorators import method_decorator
from Terminplaner.decorator import authenticated_user, who_am_i


@method_decorator(who_am_i(), name='dispatch')
class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        calendars = Calendar.objects.all()
        context['calendars'] = calendars
        user = self.object
        current_time = timezone.now()
        
        ### Hier weitermachen mit Delete integration
        from_calendar = self.request.GET.get('fC', None)
        event_to_delete = self.request.GET.get('dE', None)

        if from_calendar and event_to_delete :
            if delete_event(from_calendar,event_to_delete):
                messages.add_message(self.request, messages.SUCCESS, 'Reservation gelöscht')
            else:
                messages.add_message(self.request, messages.WARNING, 'Reservation konnte nicht gelöscht werden')

        events_by_calendar = []
        for calendar in calendars:
            events_of_calendar = Event.objects.filter(user=user, start_time__gt=current_time, calendar=calendar) 
            if bool(events_of_calendar):
                events_by_calendar.append(events_of_calendar) 
        context['events_by_calendar'] = events_by_calendar 

        return context
