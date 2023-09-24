from django.http import HttpResponseForbidden, HttpResponseRedirect
from functools import wraps
from django.shortcuts import redirect


def authenticated_user():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs) 
            else:
                if request.method == 'POST':
                    redirect(request.META.get('HTTP_REFERER', None))
                else:
                   return func(request, *args, **kwargs)  
                    
        return wrapper
    return decorator

def no_further_details():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs) 
            else:
                return redirect(request.META.get('HTTP_REFERER', None))       
        return wrapper
    return decorator

def who_am_i():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if int(request.path.split('/')[2]) == request.user.id:
                return func(request, *args, **kwargs) 
            else:
                return redirect('/')  
        return wrapper
    return decorator


