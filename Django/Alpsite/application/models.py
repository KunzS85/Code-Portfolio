from django.db import models
from django.contrib.auth.models import User


class Userinfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobil = models.CharField(max_length=14, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    street_nr = models.IntegerField(null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    self_description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural  =  "Benutzer-Informationen"