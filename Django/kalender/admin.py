from django.contrib import admin
from .models import Event, ClosedDay, Calendar, ClosedTimeWindow, Rule


class EventAdmin(admin.ModelAdmin):
    pass

class ClosedTimeWondowAdmin(admin.ModelAdmin):
    pass

class ClosedDaysAdmin(admin.ModelAdmin):
    pass

class CalendarAdmin(admin.ModelAdmin):
    pass

class RuleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Calendar,CalendarAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(ClosedDay,ClosedDaysAdmin)
admin.site.register(ClosedTimeWindow, ClosedTimeWondowAdmin)
admin.site.register(Rule, RuleAdmin)
