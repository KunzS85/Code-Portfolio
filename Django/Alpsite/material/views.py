from typing import Any, Dict
import json
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from .forms import MaterialForm
from django.views.generic import  FormView
from alpsite.decorator import you_shall_not_pass
from.models import Item


@method_decorator(you_shall_not_pass(), name='dispatch')
class MaterialPage(FormView):
    form_class = MaterialForm
    template_name = "material/material.html"
    success_url = "/material/"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        item_completed = self.request.GET.get('empty', None)
        item_refilled = self.request.GET.get('refill', None)
        item_to_kill = self.request.GET.get('kill', None)

        if item_completed:
            item = Item.objects.filter(id=item_completed)
            if item:
                item[0].completed = True
                item[0].save()
        if item_refilled:
            item = Item.objects.filter(id=item_refilled)
            if item:
                item[0].completed = False
                item[0].save()
        if item_to_kill: 
            item = Item.objects.filter(id=item_to_kill)
            if item:
                item[0].delete()


        context['existing_items'] = Item.objects.filter(completed=False)
        context['empty_items'] = Item.objects.filter(completed=True)

        return context
    
    def form_valid(self, form: Any) -> HttpResponse:

        data = form.cleaned_data

        item = data['item'] 

        new_item_data = {
            'title': item,
            'completed': False
        }

        new_item = Item(**new_item_data)
        new_item.save() 

        return super().form_valid(form)
    
    def get_success_url(self) -> str:

        return super().get_success_url()