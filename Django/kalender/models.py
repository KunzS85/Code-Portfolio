from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

EVENT_DECLARATIONS = (
    ('Training', 'Training'),
    ('Reitstunde', 'Reitstunde'),
)

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
    )
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, default=1)
    use_type = models.CharField(max_length=50, choices=EVENT_DECLARATIONS, default='Training')

    def __str__(self) -> str:
        return f"Im {self.calendar.name} für {self.user.username} von {self.start_time} bis {self.end_time} wegen {self.use_type}"
    
class ClosedTimeWindow(models.Model):
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now) 
    reason = models.TextField()
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return f"{self.calendar.name} gesperrt am {self.start_time} wegen {self.reason}"


class ClosedDay(models.Model):
    datum = models.DateField()
    reason = models.TextField()
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return f"{self.calendar.name} gesperrt am {self.datum} wegen {self.reason}"
    
class Calendar(models.Model):
    name = models.TextField()
    open_from = models.TimeField()
    open_till = models.TimeField()
    persons_per_slot = models.IntegerField()
    color_json = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"{self.name}"
    
class Rule(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.text[0:30]}"

