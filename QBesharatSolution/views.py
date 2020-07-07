from django.contrib import messages
from django.shortcuts import redirect
from QBesharatSolution.utlis import update_operator


def start_support(request):
    try:
        update_operator(request, 'ready')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
    return redirect(request.META['HTTP_REFERER'])


def stop_support(request):
    try:
        update_operator(request, 'off')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
    return redirect(request.META['HTTP_REFERER'])
