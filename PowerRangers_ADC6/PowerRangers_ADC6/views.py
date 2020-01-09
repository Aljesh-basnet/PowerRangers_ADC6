

from django.http import HttpResponse
from django.shortcuts import render

def hello_world_view(request):
    return HttpResponse("<h1>Hello world<h1>")