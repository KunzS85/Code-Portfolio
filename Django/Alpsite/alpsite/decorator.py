from django.http import HttpResponseForbidden, HttpResponseRedirect
from functools import wraps
from django.shortcuts import redirect

def you_shall_not_pass():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs) 
            else:
                return redirect('/login/')    
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

def staff_required():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.is_staff:
                return func(request, *args, **kwargs)
            else:
                return redirect('/login/') 
        return wrapper
    return decorator