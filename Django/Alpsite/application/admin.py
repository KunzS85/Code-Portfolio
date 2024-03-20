from django.contrib import admin
from .models import Userinfo

class UserinfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Userinfo, UserinfoAdmin)