from django.views.generic import  RedirectView
from django.contrib.auth import logout
from alpsite import settings


class LogOutView(RedirectView):
    url = settings.LOGOUT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)
