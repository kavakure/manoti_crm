from django.shortcuts import render
from django.http import HttpResponse

from .models import ThirdParty, Contact

def dahshboard(request):
    return render(request, "dashboard.html")

def third_party_homepage(request):
    """
    THis is the homepage for the commerce area,
    it will list the most recent third parties and contacts
    """
    third_parties = ThirdParty.objects.all().order_by('-date_added')[:15]
    contacts = Contact.objects.all().order_by('-date_added')[:15]
    return render(request, "third_party_home.html", {"third_parties": third_parties, "contacts": contacts})

def list_third_parties(request):
    """
    List all the Third parties of a given business
    """
    third_parties = ThirdParty.objects.all().order_by('-date_added')
    return render(request, "third_party_list.html", {"third_parties": third_parties})