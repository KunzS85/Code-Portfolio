from typing import Any, Dict
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import  DetailView
from alpsite.decorator import who_am_i
from django.contrib.auth.models import User
from reservation.utils import delete_reservation
from reservation.models import Reservation

@method_decorator(who_am_i(), name='dispatch')
class UserProfilePage(DetailView):
    http_method_names = ["get"]
    template_name = "userprofile/userprofile.html"
    model = User
    context_object_name = "user"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.object
        current_time = timezone.now()
        binding_time = current_time + timedelta(days=14)

        ### Delete Future Reservation ###
        reservation_to_delete_id = self.request.GET.get('delete', None)
        if reservation_to_delete_id:
            if delete_reservation(reservation_to_delete_id):
                messages.add_message(self.request, messages.SUCCESS, 'Reservation gelöscht')
            else:
                messages.add_message(self.request, messages.WARNING, 'Fehler beim Löschen')

        ### Different Reservationlists ###
        past = Reservation.objects.filter(user=user, to_date__lte=current_time)
        current = Reservation.objects.filter(user=user, from_date__lte=current_time, to_date__gte=current_time)
        future_duty = Reservation.objects.filter(user=user, from_date__gte=current_time, from_date__lte=binding_time)
        future = Reservation.objects.filter(user=user, from_date__gte=binding_time)
        if past:
            context["past_reservations"] = past
        if current:
            context["current_reservations"] = current[0]
        if future:
            context["future_reservations"] = future
        if future_duty:
            context["future_duty_reservations"] = future_duty

        return context

