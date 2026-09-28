import functools
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Administrator privileges required.')
        return redirect('dashboard')
    return wrapper

def doctor_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_doctor or request.user.is_admin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Doctor access only.')
        return redirect('dashboard')
    return wrapper

def receptionist_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_receptionist or request.user.is_admin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Receptionist / Front Desk access only.')
        return redirect('dashboard')
    return wrapper

def lab_tech_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_lab_technician or request.user.is_admin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Lab Technician access only.')
        return redirect('dashboard')
    return wrapper

def staff_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff_member or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access Denied: Staff login required.')
        return redirect('login')
    return wrapper
