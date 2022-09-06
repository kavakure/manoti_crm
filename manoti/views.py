from django.shortcuts import render
from django.http import HttpResponse

# from .models import Greeting

def dahshboard(request):
    return render(request, "dashboard.html")