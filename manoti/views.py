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

#Time related imports
from django.utils import timezone
from datetime import datetime


from .models import ThirdParty, Contact, Proposal, PurchaseOrder, ProposalLine
from .forms import ThirdPartyForm, ContactForm, ProposalForm, ProposalLineForm, ProposalStatusForm
from .utils import generate_proposal_reference

def dahshboard(request):
	return render(request, "dashboard.html")

def third_party_homepage(request):
	"""
	THis is the homepage for the Third-party area,
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
			print("[ERROR] >> %s" % third_party_form.errors) # To-do: add logging to the console

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
			messages.success(request, _('Succcessfully saved changes to the the Third-party'), extra_tags='alert alert-success alert-dismissable')
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
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
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
			contact = Contact.objects.get(id=contact_id)
			contact.delete()
			messages.success(request,  _('Succcessfully deleted the contact'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('list_contacts'))
	else:
		return http.HttpResponseRedirect(reverse('list_contacts'))
contact_delete = login_required(contact_delete)

def contact_change_status(request, contact_id=None):
	"""Changes the status of the contact"""

	try:
		contact = Contact.objects.get(id=contact_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		contact = None
		return http.HttpResponseRedirect(reverse('list_contacts'))
	
	if contact != None:
		if request.method == 'POST':
			if contact.is_active:
				contact.is_active = False
			else:
				contact.is_active = True

			contact.save()
			messages.success(request,  _('Succcessfully disabled the contact'), extra_tags='alert alert-success alert-dismissable')

			return http.HttpResponseRedirect(reverse('contact_view', kwargs={'contact_id': contact.id}))
		else:
			return http.HttpResponseRedirect(reverse('list_contacts'))
contact_change_status = login_required(contact_change_status)


def contact_create(request):
	"""Creates a contact"""
	next_url = request.GET.get('next',None)
	contact = None

	if request.method == 'POST':
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			contact = contact_form.save(commit=False)
			contact.save() # Now you can send it to DB
			messages.success(request, _('Succcessfully saved created the contact'), extra_tags='alert alert-success alert-dismissable')
			if next_url:
				return http.HttpResponseRedirect(reverse('next_url'))
			else:
				return http.HttpResponseRedirect(reverse('contact_view', kwargs={'contact_id': contact.id}))

	else:
		contact_form = ContactForm()
	return render(request, 'contact_form.html', {'contact_form': contact_form})
contact_create = login_required(contact_create)




def contact_edit(request, contact_id=None):
	"""This view is used to modify a contact"""

	if contact_id:
		editing = True
		contact = get_object_or_404(Contact, id=contact_id)
	else:
		return http.HttpResponseRedirect(reverse('contact_list'))

	initial_data = {}
	next_url = request.GET.get('next',None)

	if request.POST and contact_id:
		contact = get_object_or_404(Contact, id=contact_id)
		initial_data = model_to_dict(contact, fields=[], exclude=['date_added'])
		contact_form = ContactForm(request.POST or None, request.FILES or None, instance=contact)
		if contact_form.is_valid():
			contact_form.save()
			messages.success(request, _('Succcessfully saved changes to the contact'), extra_tags='alert alert-success alert-dismissable')
			return http.HttpResponseRedirect(reverse('contact_view', kwargs={'contact_id': contact.id}))
	else:
		contact_form = ContactForm(request.POST or None, request.FILES or None, instance=contact)

	ctx = {
		'contact_form':contact_form,
		'editing': editing,
		'contact': contact, 
		'next': next_url
	}

	return render(request, 'contact_form.html', ctx)
contact_edit = login_required(contact_edit)



##################################################################################################
### Commerce area ralated views
##################################################################################################


def commerce_homepage(request):
	"""
	This is the homepage for the commerce area,
	it will list the most recent commercials proposals, contracts and.or subscriptions
	"""
	proposals = Proposal.objects.all().order_by('-timestamp')[:15]
	customers_prospects = ThirdParty.objects.filter(is_vendor=False).order_by('-date_added')[:15]
	vendors = ThirdParty.objects.filter(is_vendor=True).order_by('-date_added')[:10]
	purchase_orders = PurchaseOrder.objects.all().order_by('-timestamp')[:10]

	ctx = {
		'proposals':proposals,
		'vendors':vendors,
		'purchase_orders':purchase_orders,
		'customers_prospects': customers_prospects
	}
	return render(request, "commerce_home.html", ctx)


def proposal_list(request):
	"""
	List all the commerical proposals of a given business
	"""
	proposals = Proposal.objects.all().order_by('-timestamp')
	return render(request, "proposal_list.html", {"proposals": proposals})

def proposal_view(request, proposal_id=None):
	"""
	View a commercial proposal by it's ID
	 """
	errors = [m for m in get_messages(request) if m.level == constants.ERROR]

	proposal   = get_object_or_404(Proposal, id=proposal_id)
	line_form  = ProposalLineForm()
	clone_form = ProposalForm()
	status_from = ProposalStatusForm()

	if errors:
		error_message = errors[0]
	else:
		error_message = None

	ctx = {
		'proposal': proposal,
		'line_form': line_form,
		'clone_form': clone_form,
		'status_from': status_from,
		'error_message' : error_message,
	}
	return render(request, "proposal_view.html", ctx)

def proposal_create(request):
	"""This view is used on order to create a commercial proposal"""
	next_url = request.GET.get('next',None)
	proposal_entry = None
	ref = generate_proposal_reference()

	if request.method == 'POST':
		proposal_form = ProposalForm(request.POST)
		if proposal_form.is_valid():
			proposal = proposal_form.save(commit=False)
			proposal.author = request.user # Set the user object here
			proposal.reference_number = ref['draft_number']
			proposal.reference  = "PROV%s" % str(ref['draft_number']).zfill(3)
			proposal.save() # Now you can send it to DB
			messages.success(request, _('Succcessfully saved created a draft commercial proposal'), extra_tags='alert alert-success alert-dismissable')
			if next_url:
				return http.HttpResponseRedirect(reverse('next_url'))
			else:
				return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))

	else:
		proposal_form = ProposalForm()
	return render(request, 'proposal_form.html', {'proposal_form': proposal_form})
proposal_create = login_required(proposal_create)


def proposal_edit(request, proposal_id=None):
	"""This view is used to modify a commercial proposal"""

	if proposal_id:
		editing = True
		proposal = get_object_or_404(Proposal, id=thirdparty_id)
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))

	initial_data = {}
	next_url = request.GET.get('next',None)

	if request.POST and thirdparty_id:
		thirdparty = get_object_or_404(ThirdParty, id=thirdparty_id)
		initial_data = model_to_dict(thirdparty, fields=[], exclude=['date_added'])
		third_party_form = ThirdPartyForm(request.POST or None, request.FILES or None, instance=thirdparty)
		if third_party_form.is_valid():
			third_party_form.save()
			messages.success(request, _('Succcessfully saved changes to the the Third-party'), extra_tags='alert alert-success alert-dismissable')
			return http.HttpResponseRedirect(reverse('third_party_view', kwargs={'thirdparty_id': thirdparty.id}))
	else:
		third_party_form = ThirdPartyForm(request.POST or None, request.FILES or None, instance=thirdparty)

	ctx = {
		'third_party_form':third_party_form,
		'editing': editing,
		'thirdparty': thirdparty, 
		'next': next_url
	}

	return render(request, 'proposal_form.html', ctx)
proposal_edit = login_required(proposal_edit)

def proposal_delete(request, proposal_id=None):
	"""Deletes a commrercial proposal from the database"""

	if request.method == 'POST':
		try:
			proposal = Proposal.objects.get(id=proposal_id)
			proposal.delete()
			messages.success(request,  _('Succcessfully deleted the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_list'))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
proposal_delete = login_required(proposal_delete)

def proposal_clone(request, proposal_id=None):
	"""Creates a commrercial proposal clone from the database"""

	if request.method == 'POST':
		try:
			proposal = Proposal.objects.get(id=proposal_id)
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
			proposal = None
			return http.HttpResponseRedirect(reverse('proposal_list'))

		if proposal != None:
			proposal_form = ProposalForm(request.POST)
			if proposal_form.is_valid():
				clone = Proposal(
					author 			= request.user,
					reference_number= generate_proposal_reference()['draft_number'],
					third_party 	= proposal_form.cleaned_data['third_party'],
					timestamp 		= timezone.now(),
					validity_duration = proposal.validity_duration,
					payment_terms	= proposal.payment_terms,
					payment_type 	= proposal.payment_type,
					source 			= proposal.source,
					availability_delay = proposal.availability_delay,
					shipping_metod 	= proposal.shipping_metod,
					delivery_date 	= proposal.delivery_date,
					document_template = proposal.document_template,
					note_private 	= proposal.note_private,
					note_public 	= proposal.note_public,
					amount_excl_tax = proposal.amount_excl_tax,
					tax 			= proposal.tax,
					amount_incl_tax = proposal.amount_incl_tax,
					is_signed 		= proposal.is_signed,
				)
				clone.reference  = "PROV%s" % str(clone.reference_number).zfill(3)
				clone.save()
				for line in proposal.proposalline_set.all():
					clone_line = ProposalLine(
						proposal = clone,
						line_type = line.line_type,
						description = line.description,
						sales_tax = line.sales_tax,
						quantity = line.quantity,
						unit_price = line.unit_price,
						discount = line.discount,
						total_tax_excl = line.total_tax_excl,
						total_tax_incl = line.total_tax_incl,

					)
					clone_line.save()

				return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': clone.id}))
			else:
				print("[ERROR] >> %s" % proposal_form.errors) # To-do: add logging to the console
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
proposal_clone = login_required(proposal_clone)

def proposal_toggle_validation(request, proposal_id=None):
	"""Sets the status of a commrercial proposal from the database"""

	if request.method == 'POST':
		try:
			proposal = Proposal.objects.get(id=proposal_id)
			if proposal.is_validated:
				proposal.is_validated = False
				proposal.reference_number = generate_proposal_reference()['draft_number']
				proposal.reference =  "PROV%s" % str(generate_proposal_reference()['draft_number']).zfill(3)
			else:
				proposal.is_validated = True
				proposal.reference_number =  generate_proposal_reference()['validated_number']
				proposal.reference =  "PR%s-%s" % (datetime.now().strftime("%y%m"), str(generate_proposal_reference()['validated_number']).zfill(3)) 
			proposal.is_signed = None
			proposal.save()
			messages.success(request,  _('Succcessfully edited the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
proposal_toggle_validation = login_required(proposal_toggle_validation)

def proposal_set_status(request, proposal_id=None):
	"""Determines if a commercial proposal is accepted or refused by a third-party"""

	if proposal_id:
		editing = True
		proposal = get_object_or_404(Proposal, id=proposal_id)
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
		proposal = None

	next_url = request.GET.get('next',None)

	if request.POST:

		status_form = ProposalStatusForm(request.POST)
		if status_form.is_valid():
			proposal.is_signed = status_form.cleaned_data['is_signed']
			proposal.save()
			messages.success(request, _('Succcessfully changed the status of the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
			
		else:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
proposal_set_status = login_required(proposal_set_status)

def proposal_line_add(request, proposal_id=None):
	"""This view is used to add a item line to a commercial proposal"""
	proposal = None
	try:
		proposal = Proposal.objects.get(id=proposal_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_list'))

	if proposal != None:
		if request.method == 'POST':
			proposal_line_form = ProposalLineForm(request.POST)
			if proposal_line_form.is_valid():
				line = proposal_line_form.save(commit=False)
				line.proposal = proposal
				if proposal.third_party.business.sales_tax_is_used:
					line.sales_tax = 18
				else:
					line.sales_tax = 0
				line.total_tax_excl = line.unit_price * line.quantity
				line.save() # Now you can send it to DB

				proposal.amount_excl_tax = 0
				for item in ProposalLine.objects.filter(proposal=proposal):
					proposal.amount_excl_tax +=  item.total_tax_excl

				if proposal.third_party.business.sales_tax_is_used:
					proposal.tax = proposal.amount_excl_tax*18/100
				else:
					proposal.tax = 0
				proposal.amount_incl_tax =  proposal.amount_excl_tax + proposal.tax
				proposal.save()

				messages.success(request, _('Succcessfully added a line to the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
			else:
				messages.success(request, _('Something went wrong'), extra_tags='alert alert-success alert-dismissable')
				print("[ERROR] >>> %s" % proposal_line_form.errors.as_data())


	return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
proposal_line_add = login_required(proposal_line_add)

def proposal_line_delete(request, proposal_id=None ,proposal_line_id=None):
	"""Removing a product/service line from a Commercial proposal"""

	try:
		proposal = Proposal.objects.get(id=proposal_id)
		proposal_line = ProposalLine.objects.get(id=proposal_line_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		proposal, proposal_line = None, None

	if request.method == 'POST' and proposal !=None and proposal_line!= None:
		try:
			proposal_line.delete()
			proposal.amount_excl_tax = 0
			for item in ProposalLine.objects.filter(proposal=proposal):
				proposal.amount_excl_tax +=  item.total_tax_excl

			if proposal.third_party.business.sales_tax_is_used:
				proposal.tax = proposal.amount_excl_tax*18/100
			else:
				proposal.tax = 0
			proposal.amount_incl_tax =  proposal.amount_excl_tax + proposal.tax
			proposal.save()

			messages.success(request,  _('Succcessfully deleted the line'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))
proposal_line_delete = login_required(proposal_line_delete)