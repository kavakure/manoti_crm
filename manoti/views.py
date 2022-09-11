from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.messages import constants, get_messages

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

def filtered_list_third_parties(request, thirdparty_type=None):
	"""
	List filtered Third parties of a given business by prospect/customer type
	"""
	
	if thirdparty_type == 'vendor':
		third_parties = ThirdParty.objects.filter(is_vendor=True).order_by('-date_added')
	else:
		third_parties = ThirdParty.objects.filter(prospect_customer__contains=thirdparty_type).order_by('-date_added')

	return render(request, "third_party_list.html", {"third_parties": third_parties,})




def third_party_view(request, thirdparty_id=None):
	"""
	View that displays a given third party
	 """

	errors = [m for m in get_messages(request) if m.level == constants.ERROR]

	thirdparty = get_object_or_404(ThirdParty, id=thirdparty_id)

	if errors:
		error_message = errors[0]
	else:
		error_message = None

	ctx = {
		'thirdparty': thirdparty,
		'error_message' : error_message,
	}
	return render(request, "third_party_view.html", ctx)


def list_contacts(request):
	"""
	Lists all the contacts of a given business
	"""
	contacts = Contact.objects.all().order_by('-date_added')
	return render(request, "contact_list.html", {"contacts": contacts})

def filtered_list_contact(request, thirdparty_type=None):
	"""
	List filtered contacts of a given business by prospect/customer type
	"""
	
	contacts = []

	if thirdparty_type == 'vendor':
		third_parties = ThirdParty.objects.filter(is_vendor=True).order_by('-date_added')
	else:
		third_parties = ThirdParty.objects.filter(prospect_customer__contains=thirdparty_type).order_by('-date_added')

	for thirdparty in third_parties:
		contacts.append(thirdparty.contact_set.all())

	return render(request, "contact_list.html", {"contacts": contacts})

def contact_view(request, contact_id=None):
	"""
	View that displays a given contact
	 """

	errors = [m for m in get_messages(request) if m.level == constants.ERROR]

	contact = get_object_or_404(Contact, id=contact_id)

	if errors:
		error_message = errors[0]
	else:
		error_message = None

	ctx = {
		'contact': contact,
		'error_message' : error_message,
	}
	return render(request, "contact_view.html", ctx)