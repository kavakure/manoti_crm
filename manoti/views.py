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


from .models import ThirdParty, Contact, Proposal, PurchaseOrder, ProposalLine, StatusChoices, ProposalLinkedFile, ProposalAttachedFile
from .models import VendorInvoice, CustomerInvoice
from .models import BankAccount
from .forms import ThirdPartyForm, ContactForm, ProposalForm, ProposalLineForm, ProposalStatusForm, ProposalStatusForm, ProposalLinkedFileForm, ProposalAttachedFileForm
from .forms import BankAccountForm
from .utils import generate_proposal_reference

@login_required
def dahshboard(request):
	return render(request, "dashboard.html")

@login_required
def third_party_homepage(request):
	"""
	THis is the homepage for the Third-party area,
	it will list the most recent third parties and contacts
	"""
	third_parties = ThirdParty.objects.all().order_by('-date_added')[:15]
	contacts = Contact.objects.all().order_by('-date_added')[:15]
	return render(request, "third_party_home.html", {"third_parties": third_parties, "contacts": contacts})

@login_required
def list_third_parties(request):
	"""
	List all the Third parties of a given business
	"""
	third_parties = ThirdParty.objects.all().order_by('-date_added')
	return render(request, "third_party_list.html", {"third_parties": third_parties})

@login_required
def filtered_list_third_parties(request, thirdparty_type=None):
	"""
	List filtered Third parties of a given business by prospect/customer type
	"""
	
	if thirdparty_type == 'vendor':
		third_parties = ThirdParty.objects.filter(is_vendor=True).order_by('-date_added')
	else:
		third_parties = ThirdParty.objects.filter(prospect_customer__contains=thirdparty_type).order_by('-date_added')

	return render(request, "third_party_list.html", {"third_parties": third_parties,})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def list_contacts(request):
	"""
	Lists all the contacts of a given business
	"""
	contacts = Contact.objects.all().order_by('-date_added')
	return render(request, "contact_list.html", {"contacts": contacts})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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


##################################################################################################
### Commerce area ralated views
##################################################################################################

@login_required
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

@login_required
def proposal_list(request):
	"""
	List all the commerical proposals of a given business or filter them by a given keyword
	"""

	is_validated_filter = request.GET.get('is_validated',None)
	is_signed = request.GET.get('is_signed',None)
	is_billed = request.GET.get('is_billed',None)

	proposals = []

	if is_validated_filter == '1': # filter the commercial proposal list by validation status
		proposals = Proposal.objects.filter(is_validated=True).order_by('-timestamp')

	elif is_validated_filter == '0':
		proposals = Proposal.objects.filter(is_validated=False).order_by('-timestamp')

	elif is_signed == '1': # filter the commercial proposal list by signed status
		proposals = Proposal.objects.filter(is_validated=True, is_signed=StatusChoices.objects.get(value=1)).exclude(is_billed=True).order_by('-timestamp')

	elif is_signed == '0': # filter the commercial proposal list by signed status
		proposals = Proposal.objects.filter(is_validated=True, is_signed=StatusChoices.objects.get(value=0)).exclude(is_billed=True).order_by('-timestamp')

	elif is_billed: # filter the commercial proposal list by signed status
		proposals = Proposal.objects.filter(is_billed=True).order_by('-timestamp')

	else:
		proposals = Proposal.objects.all().order_by('-timestamp')

	return render(request, "proposal_list.html", {"proposals": proposals})

@login_required
def proposal_view(request, proposal_id=None):
	"""
	View a commercial proposal by it's ID
	 """
	errors = [m for m in get_messages(request) if m.level == constants.ERROR]

	proposal   = get_object_or_404(Proposal, id=proposal_id)
	line_form  = ProposalLineForm()
	clone_form = ProposalForm()
	status_from = ProposalStatusForm()

	linked_file = ProposalLinkedFile(proposal=proposal)
	link_form = ProposalLinkedFileForm(instance=linked_file)

	attached_file = ProposalAttachedFile(proposal=proposal)
	attached_form = ProposalAttachedFileForm(instance=attached_file)
	

	if errors:
		error_message = errors[0]
	else:
		error_message = None

	ctx = {
		'proposal': proposal,
		'line_form': line_form,
		'clone_form': clone_form,
		'status_from': status_from,
		'link_form': link_form,
		'attached_form': attached_form,
		'error_message' : error_message,
	}
	return render(request, "proposal_view.html", ctx)

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def proposal_toggle_billing_status(request, proposal_id=None):
	"""Determines if a relative invoice was issued to the thirparty of this commrercial proposal"""

	try:
		proposal = Proposal.objects.get(id=proposal_id)
		if proposal.is_billed:
			proposal.is_billed = False
		else:
			proposal.is_billed = True
		proposal.save()
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_list'))

@login_required
def proposal_linked_file_delete(request, proposal_id=None, linked_file_id=None):
	"""Removing a linked file from a Commercial proposal"""

	try:
		proposal = Proposal.objects.get(id=proposal_id)
		linked_file = ProposalLinkedFile.objects.get(id=linked_file_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		proposal, linked_file = None, None

	if request.method == 'POST' and proposal !=None and linked_file!= None:
		try:
			linked_file.delete()
			messages.success(request,  _('Succcessfully deleted the linked file'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))

@login_required
def proposal_linked_file_add(request, proposal_id=None):
	"""This view is used to add a linked file to a commercial proposal"""
	proposal = None

	try:
		proposal = Proposal.objects.get(id=proposal_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_list'))

	if proposal != None:
		if request.method == 'POST':
			proposal_linked_file_form = ProposalLinkedFileForm(request.POST)
			if proposal_linked_file_form.is_valid():
				link = proposal_linked_file_form.save(commit=False)
				link.timestamp = timezone.now()
				link.save() # Now you can send it to DB
				messages.success(request, _('Succcessfully added a linked file to the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
			else:
				messages.success(request, _('Something went wrong'), extra_tags='alert alert-success alert-dismissable')
				print("[ERROR] >>> %s" % proposal_linked_file_form.errors.as_data())


	return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))

@login_required
def proposal_attached_file_delete(request, proposal_id=None, attached_file_id=None):
	"""Removing an attached file from a Commercial proposal"""

	try:
		proposal = Proposal.objects.get(id=proposal_id)
		attached_file = ProposalAttachedFile.objects.get(id=attached_file_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		proposal, attached_file = None, None

	if request.method == 'POST' and proposal !=None and attached_file!= None:
		try:
			attached_file.delete()
			messages.success(request,  _('Succcessfully deleted the attached file from the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
		except Exception as e:
			print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))
	else:
		return http.HttpResponseRedirect(reverse('proposal_list'))

@login_required
def proposal_attached_file_add(request, proposal_id=None):
	"""This view is used to add a file as an attachment to a commercial proposal"""
	proposal = None

	try:
		proposal = Proposal.objects.get(id=proposal_id)
	except Exception as e:
		print("[ERROR] >> %s" % e) # To-do: add logging to the console
		return http.HttpResponseRedirect(reverse('proposal_list'))

	if proposal != None:

		attached_file_form = ProposalAttachedFileForm(request.POST or None,
								 request.FILES or None)

		if request.method == 'POST':
			if attached_file_form.is_valid():
				attachment = attached_file_form.save(commit=False)
				doc_file = request.FILES['attachment']
				attachment.timestamp = timezone.now()
				attachment.save() # Now you can send it to DB
				messages.success(request, _('Succcessfully attached a file to the commercial proposal'), extra_tags='alert alert-success alert-dismissable')
			else:
				messages.success(request, _('Something went wrong'), extra_tags='alert alert-success alert-dismissable')
				print("[ERROR] >>> %s" % attached_file_form.errors.as_data())


	return http.HttpResponseRedirect(reverse('proposal_view', kwargs={'proposal_id': proposal.id}))

##################################################################################################
### Billing area ralated views
##################################################################################################

@login_required
def billing_homepage(request):
	"""
	This is the homepage for the billing and payment area,
	"""
	vendor_invoices = VendorInvoice.objects.all().order_by('-date')[:15]
	customer_invoices = CustomerInvoice.objects.all().order_by('-date')[:15]
	return render(request, "billing_home.html", {"vendor_invoices": vendor_invoices, "customer_invoices": customer_invoices})






##################################################################################################
### Bank|cash area ralated views
##################################################################################################

@login_required
def bank_homepage(request):
	"""
	This is the homepage for the Bank | Cash area
	"""
	banks = BankAccount.objects.all()[:15]
	return render(request, "bank_list.html", {"banks": banks})

@login_required
def bank_view(request, bank_id=None):
	"""
	View a bank account by it's ID
	 """
	errors = [m for m in get_messages(request) if m.level == constants.ERROR]

	bank   = get_object_or_404(BankAccount, id=bank_id)
	
	if errors:
		error_message = errors[0]
	else:
		error_message = None

	ctx = {
		'bank': bank,
		'error_message' : error_message,
	}
	return render(request, "bank_view.html", ctx)


@login_required
def bank_create(request):
	"""This view is used on order to create a bank or cash account"""
	next_url = request.GET.get('next',None)
	bank_entry = None

	if request.method == 'POST':
		bank_form = BankAccountForm(request.POST)
		if bank_form.is_valid():
			bank = bank_form.save(commit=False)
			bank.author = request.user # Set the user object here
			bank.balance = bank.initial_balance # Set the user object here
			bank.save() # Now you can send it to DB
			messages.success(request, _('Succcessfully added a Bank | cash account'), extra_tags='alert alert-success alert-dismissable')
			if next_url:
				return http.HttpResponseRedirect(reverse('next_url'))
			else:
				return http.HttpResponseRedirect(reverse('bank_view', kwargs={'bank_id': bank.id}))

	else:
		bank_form = BankAccountForm()
	return render(request, 'bank_form.html', {'bank_form': bank_form})
