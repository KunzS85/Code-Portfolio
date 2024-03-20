from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Reservation(models.Model):

    creation_datetime = models.DateTimeField(default=now)
    from_date = models.DateField()
    to_date = models.DateField()
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
    )
    approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} von {self.from_date} bis {self.to_date}"
    
    class Meta:
        verbose_name_plural  =  "Reservationen"