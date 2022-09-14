from django.shortcuts import render
from django import http
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.messages import constants, get_messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.urls import reverse
from django.forms.models import model_to_dict


from .models import ThirdParty, Contact
from .forms import ThirdPartyForm

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


def third_party_create(request):
	"""This view is used on order to create a Third party"""
	next_url = request.GET.get('next',None)
	third_party_entry = None

	if request.method == 'POST':
		third_party_form = ThirdPartyForm(request.POST)
		if third_party_form.is_valid():
			thirdparty = third_party_form.save(commit=False)
			thirdparty.user = request.user # Set the user object here
			thirdparty.save() # Now you can send it to DB
			messages.success(request, _('Succcessfully saved created the third party'), extra_tags='alert alert-success alert-dismissable')
			if next_url:
				return http.HttpResponseRedirect(reverse('next_url'))
			else:
				return http.HttpResponseRedirect(reverse('third_party_view', kwargs={'thirdparty_id': thirdparty.id}))

	else:
		third_party_form = ThirdPartyForm()
	return render(request, 'third_party_form.html', {'third_party_form': third_party_form})
third_party_create = login_required(third_party_create)


def third_party_edit(request, thirdparty_id=None):
	"""This view is used to modify a Third party"""

	if thirdparty_id:
		editing = True
		thirdparty = get_object_or_404(ThirdParty, id=thirdparty_id)
	else:
		return http.HttpResponseRedirect(reverse('third_party_list'))

	initial_data = {}
	next_url = request.GET.get('next',None)

	if request.POST and thirdparty_id:
		thirdparty = get_object_or_404(ThirdParty, id=thirdparty_id)
		initial_data = model_to_dict(thirdparty, fields=[], exclude=['date_added'])
		third_party_form = ThirdPartyForm(request.POST or None, request.FILES or None, instance=thirdparty)
		if third_party_form.is_valid():
			third_party_form.save()
			messages.success(request, _('Succcessfully saved changes to your resume'), extra_tags='alert alert-success alert-dismissable')
			return http.HttpResponseRedirect(reverse('third_party_view', kwargs={'thirdparty_id': thirdparty.id}))
	else:
		third_party_form = ThirdPartyForm(request.POST or None, request.FILES or None, instance=thirdparty)

	ctx = {
		'third_party_form':third_party_form,
		'editing': editing,
		'thirdparty': thirdparty, 
		'next': next_url
	}

	return render(request, 'third_party_form.html', ctx)
third_party_edit = login_required(third_party_edit)


def third_party_delete(request, thirdparty_id=None):
	"""Deletes a Third party from the database"""

	if request.method == 'POST':
		try:
			thirdparty = ThirdParty.objects.get(id=thirdparty_id)
			thirdparty.delete()
			messages.success(request,  _('Succcessfully deleted the Third party'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print(e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('list_third_parties'))
	else:
		return http.HttpResponseRedirect(reverse('list_third_parties'))
third_party_delete = login_required(third_party_delete)


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

def contact_delete(request, contact_id=None):
	"""Deletes a contact from the database"""

	if request.method == 'POST':
		try:
			contact = ThirdParty.objects.get(id=contact_id)
			contact.delete()
			messages.success(request,  _('Succcessfully deleted the contact'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print(e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('list_contacts'))
	else:
		return http.HttpResponseRedirect(reverse('list_contacts'))
contact_delete = login_required(contact_delete)

def contact_change_status(request, contact_id=None):
	"""Changes the status of the contact"""

	try:
		contact = ThirdParty.objects.get(id=contact_id)
	except Exception as e:
		print(e) # To-do: add logging to the console
		contact = None
		return http.HttpResponseRedirect(reverse('list_contacts'))
	
	if contact != None:
		if request.method == 'POST':
			if is_active:
				contact.is_active = False
			else:
				contact.is_active = True

			contact.save()
			messages.success(request,  _('Succcessfully disabled the contact'), extra_tags='alert alert-success alert-dismissable')

			return http.HttpResponseRedirect(reverse('contact_view', kwargs={'contact_id': contact.id}))
		else:
			return http.HttpResponseRedirect(reverse('list_contacts'))
contact_change_status = login_required(contact_change_status)