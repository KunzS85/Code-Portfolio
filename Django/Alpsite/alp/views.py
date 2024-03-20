from datetime import date, time, datetime, timedelta
from typing import Any, Dict
from django.utils.safestring import mark_safe
from django.urls import reverse, re_path
from django.utils import timezone
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import  ListView, TemplateView, FormView
from django.contrib import messages
from django.db.models import Q
from alpsite.decorator import you_shall_not_pass
from .models import InformationDetail, Picture, Contact

#from .models import Event, ClosedDay, Calendar, ClosedTimeWondow


class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "alp/homepage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)


        return context


@method_decorator(you_shall_not_pass(), name='dispatch')    
class InformationPage(TemplateView):
    http_method_names = ["get"]
    template_name = "alp/information.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        all_infos = InformationDetail.objects.all()
        
        context['all_infos'] = all_infos

        return context
    
class InformationDetailPage(TemplateView):
    http_method_names = ["get"]
    template_name = "alp/information_detail.html"

    def should_redirect(self, info_detail):
        site_should_be_secure = getattr(info_detail, 'secure')
        return site_should_be_secure and not self.request.user.is_authenticated

    def dispatch(self, *args, **kwargs):
        info_detail = InformationDetail.objects.filter(id=self.kwargs['pk']).first()

        if info_detail is None:
            return super().dispatch(*args, **kwargs)

        if self.should_redirect(info_detail):
            return HttpResponseRedirect('/login/')
        else:
            return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        info_detail = InformationDetail.objects.filter(id=self.kwargs['pk']).first()

        if info_detail is None:
            return context

        info_detail_images = info_detail.images.all()
        info_detail_videos = info_detail.videos.all()

        context['details'] = info_detail
        context['images'] = info_detail_images
        context['videos'] = info_detail_videos

        return context



        

@method_decorator(you_shall_not_pass(), name='dispatch')
class GalleryPage(TemplateView):
    http_method_names = ["get"]
    template_name = "alp/gallery.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['images'] = Picture.objects.filter(is_gallery_picture=True)

        return context
    
@method_decorator(you_shall_not_pass(), name='dispatch')
class ContactPage(TemplateView):
    http_method_names = ["get"]
    template_name = "alp/contact.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['contacts'] = Contact.objects.all()

        return context
    