from django.contrib import admin
from .models import Picture, Video, InformationDetail, Contact

class PictureAdmin(admin.ModelAdmin):
    pass

class VideoAdmin(admin.ModelAdmin):
    pass

class InformationDetailAdmin(admin.ModelAdmin):
    filter_horizontal = ('images','videos',)

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Picture, PictureAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(InformationDetail, InformationDetailAdmin)
admin.site.register(Contact, ContactAdmin)