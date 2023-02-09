from django.shortcuts import render
from .tasks import logic
from django.http import HttpResponse

def index(request):
    result=logic.delay()
    # result=add(4)
    # return HttpResponse(result)
    return HttpResponse(result)

