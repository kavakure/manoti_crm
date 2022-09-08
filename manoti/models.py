from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from .validators import validate_file_size, validate_image_file_extension, validate_document_file_extension

from datetime import date
from django.utils import timezone

MONTH_CHOICES = (
	('1', _('January')),
	('2', _('February')),
	('3', _('March')),
	('4', _('April')),
	('5', _('May')),
	('6', _('June')),
	('7', _('July')),
	('8', _('August')),
	('9', _('September')),
	('10', _('October')),
	('11', _('November')),
	('12', _('December'))
)

PROSPOECT_CUSTOMER_CHOICES = (
	('prospect', _('Prospect')),
	('prospect_and_customer', _('Prospect and Customer')),
	('customer', _('Customer')),
	('none', _('Not a Prospect nor a Customer'))
)

STATUS_CHOICES = (
	('open', _('Open')),
	('closed', _('Closed'))
)

THIRD_PARTY_CHOICES = (
	('govermental', _('Govermental')),
	('large company', _('Large Company')),
	('medium company', _('Medium Company')),
	('other', _('Other')),
	('private individual', _('Private Individual')),
	('small company', _('Small Company'))
)


class StatusChoices(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key


class Business(models.Model):
	user                = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, help_text=_("The user object that owns Company/Organization"))
	name                = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The full name of your Company/Organization"))
	address             = models.TextField(_("Full Address"), blank=True, null=True, help_text=_("Please mention here the full address of your Company/Organization"))
	google_map_url      = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the Company/Organization"))
	po_box	            = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of your Company/Organization"))
	town                = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("Indicate the town address of your Company/Organization"))
	country             = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where your Company/Organization is located and/or registered"))
	state_province      = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where your Company/Organization is located and/or registered"))
	main_currency       = models.CharField(_("Main currency"), max_length=200, blank=True, default ="Fbu", help_text=_("What is the Currency used by your Company/Organization"))
	phone               = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of your Company/Organization"))
	email               = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of your Company/Organization"))
	website             = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("The website of your Company/Organization"))
	logo                = models.FileField(_("Logo"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG, will be used on various documents related to your Company/Organization"))
	logo_squarred       = models.FileField(_("Logo (squarred)"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG, used for branding accross this platform"))
	note             = models.TextField(_("Notes"), blank=True, null=True, help_text=_("Any additional note or information about the Company/Organization"))
	
	# Company/Organization identities
	manager_name        = models.CharField(_("Manager(s) name (CEO, director, president...)"), max_length=200, blank=True, help_text=_("Manager(s) name (CEO, director, president...)"))
	data_protection_officer = models.CharField(_("Data Protection Officer (DPO, Data Privacy or GDPR contact)"), max_length=200, blank=True, help_text=_("If your organisation is located in the EU, this field is required"))
	capital             = models.IntegerField(_("Capital"), blank=True, null=True)
	business_entity_type = models.CharField(_("Business entity type"), max_length=200, blank=True, null=True, help_text=_("If your organisation is located in the EU, this field is required"))
	professional_id_1   = models.CharField(_("Professional ID 1"), max_length=200, blank=True, null=True)
	professional_id_2   = models.CharField(_("Professional ID 2"), max_length=200, blank=True, null=True)
	professional_id_3   = models.CharField(_("Professional ID 3"), max_length=200, blank=True, null=True)
	professional_id_4   = models.CharField(_("Professional ID 4"), max_length=200, blank=True, null=True)
	professional_id_5   = models.CharField(_("Professional ID 5"), max_length=200, blank=True, null=True)
	professional_id_6   = models.CharField(_("Professional ID 6"), max_length=200, blank=True, null=True)
	vat_id              = models.CharField(_("VAT ID"), max_length=200, blank=True, null=True)
	registre_de_commerce = models.CharField(_("Registre de Commerce"), max_length=200, blank=True, null=True)
	object_of_the_company = models.TextField(_("Object of the company"), max_length=900, blank=True, null=True)
	
	# Fiscal Year
	fiscal_year = models.CharField(_("Starting month of the fiscal year"), blank=False, max_length=100, null=False, choices=MONTH_CHOICES, default='1')

	# Type of sales tax
	sales_tax_is_used = models.BooleanField(_("Are Sales tax used by your Company/Organization?"), default=False)

	def __str__(self):
		return self.name

class BusinessAccountant(models.Model):
	#If you have an external accountant/bookkeeper, you can edit here its information.
	business          = models.ForeignKey(Business, blank=False, null=False, on_delete=models.CASCADE,)
	name              = models.CharField(_("Full name"), max_length=200, blank=True, help_text=_("The full name of the Company/Organization's accountant"))
	address           = models.TextField(_("Full Address"), blank=True, null=True, help_text=_("Please mention here the full address of your Company/Organization's accountant"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of your Company/Organization's accountant"))
	town              = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("Indicate the town address of your Company/Organization's accountant"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where Company/Organization's accountant is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where Company/Organization's accountant is located and/or registered"))
	phone             = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of your Company/Organization's accountant"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of your Company/Organization's accountant"))
	website           = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("The website of your Company/Organization's accountant"))
	code              = models.CharField(_("Accountant code"), max_length=200, blank=True, help_text=_("The full name of the Company/Organization's accountant"))
	note           	  = models.TextField(_("Notes"), blank=True, null=True, help_text=_("Any additional note or information about the Company/Organization's accountant"))

	def __str__(self):
		return self.name

class SocialNetwork(models.Model):
	#If you have an external accountant/bookkeeper, you can edit here its information.
	business          = models.ForeignKey(Business, blank=False, null=False, on_delete=models.CASCADE,)
	name              = models.CharField(_("Social networks"), max_length=200, blank=True, help_text=_("The name of the social Network"))
	url         	  = models.URLField(_("Url"), blank=True, null=True, help_text=_("The URL of the social Network"))
	network_id        = models.CharField(_("Social Network ID"), max_length=200, blank=True, null=True, help_text=_("The social network handle or ID of your Company/Organization"))

	def __str__(self):
		return self.name

# Human Resource Management (HR)
class Employee(models.Model):
	"""
	 Users / Employees and Groups management
	 TO-DO: add Foreign key Phone number to have the ability to add mutiple Phone numbers for a given employee
	 """

	user              = models.ForeignKey(User, blank=False, related_name='employee_user', null=False, on_delete=models.CASCADE, help_text=_("The user object related to the employee"))
	last_name         = models.CharField(_("Last name"), max_length=200, blank=True)
	first_name        = models.CharField(_("First name"), max_length=200, blank=True)
	is_administrator  = models.BooleanField(_("Administrator ?"), default=False)
	is_employee 	  = models.BooleanField(_("Employee"), default=True)
	supervisor        = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Supervisor"))
	force_expense_report_validator = models.ForeignKey(User, related_name='force_expense_report_validator', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Force expense report validator"))
	force_leave_request_validator = models.ForeignKey(User, related_name='force_leave_request_validator',blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Force leave request validator"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of the employee"))
	city              = models.CharField(_("City"), max_length=200, blank=True, default="Bujumbura", help_text=_("Indicate the city ot town address of the employee"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where the employee is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where your the employee lives"))
	mobile_phone      = models.CharField(_("Mobile Phone Number"), blank=True, null=True, max_length=30, help_text=_("The mobile Phone number of the employee"))
	business_phone    = models.CharField(_("Business Phone Number"), blank=True, null=True, max_length=30, help_text=_("The office or business Phone number of the employee"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of the employee"))
	note              = models.TextField(_("Notes"), blank=True, null=True, help_text=_("Any additional note or information about the employee"))
	signature         = models.TextField(_("Signature"), blank=True, null=True)

	job_postion       = models.CharField(_("Job position"), blank=True, null=True, max_length=30)
	average_hourly_rate = models.IntegerField(_("Average hourly rate"), blank=True, null=True)
	average_daily_rate  = models.IntegerField(_("Average Daily rate"), blank=True, null=True)
	salary     		  = models.IntegerField(_("Salary"), blank=True, null=True)
	hours_worked_per_week = models.IntegerField(_("Hours worked (per week)"), blank=True, null=True)
	employement_start = models.DateField(_("Employement date begun"), blank=True, null=True, help_text=_("Ex: 01/04/2019, The date when The employee started working for the company"))
	employement_end   = models.DateField(_("Employement date ended"), blank=True, null=True, help_text=_("Ex: 01/04/2019, The date when The employee left the company"))
	date_of_birth 	  = models.DateField(_("Date of birth"), blank=True, null=True)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

# Customer Relationship Management (CRM)
	
class PhoneNumber(models.Model):
	type              = models.CharField(_("Third party name"), max_length=200, blank=True, default="Mobile", help_text=_("The type of the phone device"))
	phone_number	  = models.CharField(_("Phone Number"), blank=False, max_length=30,)

	def __str__(self):
		return self.phone_number

class BusinessEntityType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class ThirdPartyType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class ThirdParty(models.Model):
	# Companies and contacts management (customers, vendors and prospects, ...)
	business          = models.ForeignKey(Business, blank=False, null=False, on_delete=models.CASCADE)
	name              = models.CharField(_("Third party name"), max_length=200, blank=False, null=False, help_text=_("The full name of the Third Party"))
	alias_name        = models.CharField(_("Alias name (commercial, trademark, ...)"), max_length=200, blank=True, help_text=_("The Alias name used for other purposes"))
	prospect_customer = models.CharField(_("Prospect / Customer"), choices=PROSPOECT_CUSTOMER_CHOICES, max_length=200, blank=True, help_text=_("Defines which type the thirdparty is"))
	customer_code_number = models.IntegerField(_("Customer code number"), blank=True, null=True, default=1)
	customer_code     = models.CharField(_("Customer code"), max_length=200, blank=True, unique=True)
	is_vendor		  = models.BooleanField(_("Vendor ?"), default=False)
	vendor_code_number = models.IntegerField(_("Vendor code number"), blank=True, null=True, default=1)
	vendor_code       = models.CharField(_("Vendor code"), max_length=200, blank=True, null=False, unique=True)
	status 			  = models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=200, blank=False, null=False, default="open")
	barcode			  = models.CharField(_("Barcode"), max_length=200, blank=True, null=True)
	address           = models.TextField(_("Full address"), blank=True, null=True, help_text=_("The full address of the Third party"))
	google_map         = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the Third party"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of the Third party"))
	town              = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("Indicate the town address of the Third party"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where the Third party is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where the Third party is located and/or registered"))
	phone             = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of the Third party"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of the Third party"))
	website           = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("The website of the Third party"))
	professional_id_1 = models.CharField(_("Professional ID 1"), max_length=200, blank=True, null=True)
	professional_id_2 = models.CharField(_("Professional ID 2"), max_length=200, blank=True, null=True)
	professional_id_3 = models.CharField(_("Professional ID 3"), max_length=200, blank=True, null=True)
	professional_id_4 = models.CharField(_("Professional ID 4"), max_length=200, blank=True, null=True)
	professional_id_5 = models.CharField(_("Professional ID 5"), max_length=200, blank=True, null=True)
	professional_id_6 = models.CharField(_("Professional ID 6"), max_length=200, blank=True, null=True)
	vat_id            = models.CharField(_("VAT ID"), max_length=200, blank=True, null=True)
	registre_de_commerce = models.CharField(_("Registre de Commerce"), max_length=200, blank=True, null=True)
	sales_tax_is_used = models.BooleanField(_("Are Sales tax used by your Company/Organization?"), default=False)
	third_party_type  = models.ForeignKey(ThirdPartyType, verbose_name=_("Third-party type"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	business_entity_type = models.ForeignKey(BusinessEntityType, verbose_name=_("Business entity type"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	workforce		  = models.IntegerField(_("workforce"), blank=True, default=1)
	capital           = models.IntegerField(_("Capital"), blank=True, null=True)
	assigned_representative = models.ForeignKey(Employee, verbose_name=_("Assigned representative"), blank=True, null=True, on_delete=models.CASCADE)
	logo              = models.FileField(_("Logo"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG, will be used on various documents related to your Company/Organization"))
	date_added		  = models.DateField(_("Date of creation"), blank=False, default=timezone.now)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("Third party")
		verbose_name_plural = _("Third parties")

class Title(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class Contact(models.Model):
	#
	third_party 	  = models.ForeignKey(ThirdParty, verbose_name=_("Third party"), null=True, on_delete=models.CASCADE)
	last_name         = models.CharField(_("Last name / Label"), max_length=200, blank=True)
	first_name        = models.CharField(_("First name"), max_length=200, blank=True, help_text=_("Keep this field empty if this is a generic address"))
	title		 	  = models.ForeignKey(Title, verbose_name=_("title"), null=True, on_delete=models.CASCADE)
	job_title         = models.CharField(_("Job Title"), max_length=200, blank=True)
	address           = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the contact"))
	google_map        = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the contact"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of your Company/Organization"))
	town              = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("Indicate the town address of your contact"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where the contact is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where the contact is located and/or registered"))
	phone             = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The phone number of the contact"))
	bus_phone         = models.CharField(_("Business Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Office or business phone number of the contact"))
	mobile_phone      = models.CharField(_("Mobile Phone Number"), blank=True, null=True, max_length=30, help_text=_("The mobile phone number of the contact"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of the contact"))
	is_private 		  = models.BooleanField(_("Visibilty"), default=False)
	alert 			  = models.BooleanField(_("Alerts"), default=False)
	date_of_birth 	  = models.DateField(_("Date of birth"), blank=True)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class PaymentType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class PaymentTerms(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key
		
class Source(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class AvailabilityDelay(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class ShippingMetod(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class ProposalDocumentTemplate(models.Model):
	# 
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The full name of your Company/Organization"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	description       = models.TextField(_("Description"), blank=True, null=True)
	content        	  = models.TextField(_("Content of the document"), blank=True, null=True)

	def __str__(self):
		return filename

class Proposal(models.Model):
	# 
	reference      	= models.CharField(_("Reference"), max_length=200, blank=False, null=False, default="Draft")
	customer_reference = models.CharField(_("Customer reference"), max_length=200, blank=False, null=True)
	customer 	  	= models.ForeignKey(ThirdParty, verbose_name=_("Third party"), blank=False, null=True, on_delete=models.CASCADE)
	timestamp 		= models.DateField(_("Date"), blank=True, null=True, auto_now_add=True)
	validity_duration = models.IntegerField(_("Validity duration"), blank=True, null=True, default=30, help_text=_("days"))
	payment_terms 	= models.ForeignKey(PaymentTerms, verbose_name=_("Payment terms"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	payment_type 	= models.ForeignKey(PaymentType, verbose_name=_("Payment method"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	source 	  		= models.ForeignKey(Source, verbose_name=_("Source"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	availability_delay = models.ForeignKey(AvailabilityDelay, verbose_name=_("Availability delay (after order)"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	shipping_metod	= models.ForeignKey(ShippingMetod, verbose_name=_("Shipping Method"), blank=True, null=True, on_delete=models.CASCADE)
	delivery_date	= models.DateField(_("Delivery date"), blank=True)
	document_template = models.ForeignKey(ProposalDocumentTemplate, verbose_name=_("Default doc template"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	note_private    = models.TextField(_("Private note"), blank=True, null=True)
	note_public     = models.TextField(_("Public Note"), blank=True, null=True)
	#The money figures
	amount_excl_tax = models.IntegerField(_("Amount (excl. tax)"), blank=False, null=False, default=0)
	tax = models.IntegerField(_("Amount tax"), blank=False, null=False, default=0)
	amount_incl_tax = models.IntegerField(_("Amount (inc. tax)"), blank=False, null=False, default=0)
	is_validated = models.BooleanField(_("Is the commercial proposal validated"), default=False, blank=False, null=False, help_text=_("Are you sure you want to validate this commercial proposal under name PR########?"))
	status = models.ForeignKey(StatusChoices, verbose_name=_("Set accepted/refused"), null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.reference

	class Meta:
		verbose_name = _("Commercial proposal")
		verbose_name_plural = _("Commercial proposals")
		ordering = ('timestamp',)

class ProposalLinkedFile(models.Model):
	# 
	proposal 	  	  = models.ForeignKey(Proposal, verbose_name=_("Proposal"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	link       		  = models.URLField(_("Link"), blank=True, max_length=900)
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)
	save_original_name = models.BooleanField(_("Save with original file name"), default=False, help_text=_("Save file on server with name 'PR##############-Original filename' (otherwise 'Original filename')"))

	def __str__(self):
		return self.filename

class ProposalAttachedFile(models.Model):
	# 
	proposal 	  	  = models.ForeignKey(Proposal, verbose_name=_("Proposal"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)

	def __str__(self):
		return self.filename

class LineType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class ProposalLine(models.Model):
	# 
	proposal 	  	= models.ForeignKey(Proposal, verbose_name=_("Proposal"), null=True, on_delete=models.CASCADE)
	line_type 		= models.ForeignKey(LineType, verbose_name=_("Type"), null=True, on_delete=models.CASCADE)
	description     = models.TextField(_("Description"), blank=False, null=False)
	sales_tax 		= models.IntegerField(_("Sales tax"), blank=False)
	quantity 		= models.IntegerField(_("Qty"), blank=False, default=1)
	total_tax_excl 	= models.IntegerField(_("Total (Tax excl.)"))
	total_tax_incl 	= models.IntegerField(_("Total (Tax incl.)"))

	def __str__(self):
		return self.description

# ========================================================================
#Bank Accounts models
BANK_ACCOUNT_TYPE_CHOICES = (
	('savings', _('Savings account')),
	('current', _('Current or Credit Card account')),
	('cash', _('Cash account'))
)

class BankAccount(models.Model):
	# 
	business        = models.ForeignKey(Business, verbose_name=_("Bank Account"), blank=False, null=False, on_delete=models.CASCADE)
	reference       = models.CharField(_("Reference"), max_length=200, blank=False, null=False)
	account_type    = models.CharField(_("Account type"), max_length=200, blank=False, null=False, choices=BANK_ACCOUNT_TYPE_CHOICES)
	status 			= models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=200, blank=True)
	currency       	= models.CharField(_("Currency"), max_length=200, blank=True, default ="Fbu", help_text=_("What is the Currency of this financial institution"))
	country         = models.CharField(_("Account country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where the bank/financial instituion is located "))
	state_province  = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where the bank/financial instituion is located and/or registered"))
	website         = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("The website of the bank/financial instituion"))
	comment		    = models.TextField(_("Comment"), blank=True, null=True)
	initial_balance = models.IntegerField(_("Initial balance"))
	timestamp 		= models.DateField(_("Date"), blank=True)
	minimum_allowed_balance = models.IntegerField(_("Minimum allowed balance"))
	minimum_desired_balance = models.IntegerField(_("Minimum desired balance"))
	name            = models.CharField(_("Bank name"), max_length=200, blank=True, null=True)
	account_number  = models.CharField(_("Account number"), max_length=200, blank=True, null=True)
	iban_number     = models.CharField(_("IBAN account number"), max_length=200, blank=True, null=True)
	swift           = models.CharField(_("IBAN account number"), max_length=200, blank=True, null=True)
	address         = models.TextField(_("Bank address"), blank=True, null=True, help_text=_("Please mention here the full address of the financial institution"))
	account_owner_name = models.CharField(_("Account owner name"), max_length=200, blank=True, null=True)
	account_owner_address = models.TextField(_("account owner address"), blank=True, null=True, help_text=_("Please mention here the full address of the financial institution"))

	def __str__(self):
		return self.reference
		
class BankAccountLinkedFile(models.Model):
	# 
	bank 		  	  = models.ForeignKey(BankAccount, verbose_name=_("Bank Account"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	link       		  = models.URLField(_("Link"), blank=True, max_length=900)
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)
	save_original_name = models.BooleanField(_("Save with original file name"), default=False, help_text=_("Save file on server with name 'PR##############-Original filename' (otherwise 'Original filename')"))

	def __str__(self):
		return self.filename

class BankAccountAttachedFile(models.Model):
	# 
	bank 	 	  	  = models.ForeignKey(BankAccount, verbose_name=_("Bank Account"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)

	def __str__(self):
		return self.filename

SENS_CHOICES = (
    (-1, 'Credit'),
    (1, 'Debit'),
)

class BankEntry(models.Model):
	# 
	date 	  		  = models.DateField(_("Date"), blank=True)
	value_date 	 	  = models.DateField(_("value date"), blank=True)
	label          	  = models.CharField(_("Label"), max_length=200, blank=True, default="Miscellaneous payment")
	amount 			  = models.IntegerField(_("Amount"))
	bank 	  	  	  = models.ForeignKey(BankAccount, verbose_name=_("Bank Account"), null=True, on_delete=models.CASCADE)
	payment_type 	  = models.ForeignKey(PaymentType, verbose_name=_("Payment Type"), null=True, on_delete=models.CASCADE)
	check_transfer_number = models.CharField(_("Number (Check/Transfer N°)"), max_length=200, blank=True)
	check_transfer_sender = models.CharField(_("Sender (Check/Transfer sender)"), max_length=200, blank=True)
	bank_of_check 	  = models.CharField(_("Bank (Bank of Check)"), max_length=200, blank=True)
	accounting_account  = models.CharField(_("Accounting account"), max_length=200, blank=True)
	subledger_account = models.CharField(_("Subledger account"), max_length=200, blank=True)
	sens 			  = models.FloatField(_("Sens"), choices=SENS_CHOICES, help_text=_("For an accounting account of a customer, use Credit to record a payment you have received\nFor an accounting account of a supplier, use Debit to record a payment you made"))
	
	def __str__(self):
		return self.label

# ========================================================================
# Billing and payment area

VENDOR_INVOICE_CHOICES = (
	("standard", 'Standard invoice'),
    ("downpayment", 'Downpayment invoice'),
    ("credit", 'Credit Note'),
)

class VendorInvoice(models.Model):
	# 
	reference      		= models.CharField(_("Reference"), max_length=200, blank=False, null=False, default="Draft", unique=True)
	third_party 	  	= models.ForeignKey(ThirdParty, verbose_name=_("Vendor"), blank=False, null=False, on_delete=models.CASCADE)
	vendor_reference    = models.CharField(_("Reference Vendor"), max_length=200, blank=False, null=False, default="Draft")
	vendor_invoice_type = models.CharField(_("Status"), choices=VENDOR_INVOICE_CHOICES, default="standard", max_length=200, blank=False, null=False)
	label          	  	= models.CharField(_("Label"), max_length=200, blank=True)
	date 	  		  	= models.DateField(_("Invoice date"), blank=False, null=False)
	payment_due		  	= models.DateField(_("Payment due on"), blank=True, null=True)
	payment_terms 		= models.ForeignKey(PaymentTerms, verbose_name=_("Payment terms"), null=True, on_delete=models.CASCADE)
	payment_type 		= models.ForeignKey(PaymentType, verbose_name=_("Payment type"), null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	bank_account 		= models.ForeignKey(BankAccount, verbose_name=_("Bank account"), null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	note_private    	= models.TextField(_("Private note"), blank=True, null=True)
	note_public     	= models.TextField(_("Public Note"), blank=True, null=True)
	total_tax_excl 		= models.IntegerField(_("Amount (excl. tax)"), default=0)
	tax_amount 	  		= models.IntegerField(_("Amount tax"), default=0)
	total_tax_incl 	  	= models.IntegerField(_("Amount (inc. tax)"), default=0)
	total_payment 	  	= models.IntegerField(_("Amount (inc. tax)"), default=0)
	is_validated		= models.BooleanField(_("Validated ?"), default=False)
	is_abandoned		= models.BooleanField(_("Abandoned ?"), default=False)

	def __str__(self):
		return self.reference

class VendorInvoiceLinkedFile(models.Model):
	# 
	vendor_invoice 	   = models.ForeignKey(VendorInvoice, verbose_name=_("Vendor invoice"), null=True, on_delete=models.CASCADE)
	filename           = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	link       		   = models.URLField(_("Link"), blank=True, max_length=900)
	timestamp 		   = models.DateField(_("Timestamp"), blank=True)
	save_original_name = models.BooleanField(_("Save with original file name"), default=False, help_text=_("Save file on server with name 'PR##############-Original filename' (otherwise 'Original filename')"))

	def __str__(self):
		return self.filename

class VendorInvoiceAttachedFile(models.Model):
	# 
	vendor_invoice 	  = models.ForeignKey(VendorInvoice, verbose_name=_("Vendor invoice"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)

	def __str__(self):
		return self.filename

class VendorInvoiceLine(models.Model):
	# 
	vendor_invoice 	  = models.ForeignKey(VendorInvoice, verbose_name=_("Vendor invoice"), null=True, on_delete=models.CASCADE)
	line_type 		  = models.ForeignKey(LineType, verbose_name=_("Type"), null=True, on_delete=models.CASCADE)
	description       = models.TextField(_("Description"), blank=False, null=False)
	sku		          = models.CharField(_("Vendor SKU"), max_length=200, blank=True)
	sales_tax 		  = models.IntegerField(_("Sales tax"), blank=False)
	unit_price_tax_excl = models.IntegerField(_("Unit price (net)"))
	unit_price_tax_incl = models.IntegerField(_("Unit price (Tax incl.)"))
	discount 		  = models.IntegerField(_("Discount"), blank=True, default=0)
	quantity 		  = models.IntegerField(_("Qty"), blank=False, default=1)

	def __str__(self):
		return self.description

class VendorInvoiceContactType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class VendorInvoiceContact(models.Model):
	# 
	vendor_invoice 	  = models.ForeignKey(VendorInvoice, verbose_name=_("Vendor invoice"), null=True, on_delete=models.CASCADE)
	third_party  	  = models.ForeignKey(ThirdParty, verbose_name=_("Third-party"), blank=True, null=True, on_delete=models.CASCADE)
	contact  		  = models.ForeignKey(Contact, verbose_name=_("Users | Contacts/Addresses"), blank=True, null=True, on_delete=models.CASCADE)
	contact_type  	  = models.ForeignKey(VendorInvoiceContactType, verbose_name=_("Users | Contacts/Addresses"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))

	def __str__(self):
		return self.contact

CUSTOMER_INVOICE_CHOICES = (
	("standard", 'Standard invoice'),
    ("downpayment", 'Downpayment invoice'),
    ("replacement", 'Replacement invoice'),
    ("credit", 'Credit Note'),
    ("template", 'Template Invoice'),
)

class CustomerInvoice(models.Model):
	# 
	reference      		= models.CharField(_("Reference"), max_length=200, blank=False, null=False, default="Draft", unique=True)
	third_party 	  	= models.ForeignKey(ThirdParty, verbose_name=_("Customer"), blank=False, null=False, on_delete=models.CASCADE)
	customer_reference    = models.CharField(_("Reference Vendor"), max_length=200, blank=False, null=False, default="Draft")
	customer_invoice_type = models.CharField(_("Status"), choices=VENDOR_INVOICE_CHOICES, default="standard", max_length=200, blank=False, null=False)
	label          	  	= models.CharField(_("Label"), max_length=200, blank=True)
	date 	  		  	= models.DateField(_("Invoice date"), blank=False, null=False)
	payment_due		  	= models.DateField(_("Payment due on"), blank=True, null=True)
	payment_terms 		= models.ForeignKey(PaymentTerms, verbose_name=_("Payment terms"), null=True, on_delete=models.CASCADE)
	payment_type 		= models.ForeignKey(PaymentType, verbose_name=_("Payment type"), null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	bank_account 		= models.ForeignKey(BankAccount, verbose_name=_("Bank account"), null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))
	note_private    	= models.TextField(_("Private note"), blank=True, null=True)
	note_public     	= models.TextField(_("Public Note"), blank=True, null=True)
	total_tax_excl 		= models.IntegerField(_("Amount (excl. tax)"), default=0)
	tax_amount 	  		= models.IntegerField(_("Amount tax"), default=0)
	total_tax_incl 	  	= models.IntegerField(_("Amount (inc. tax)"), default=0)
	total_payment 	  	= models.IntegerField(_("Amount (inc. tax)"), default=0)
	is_validated		= models.BooleanField(_("Validated ?"), default=False)
	is_abandoned		= models.BooleanField(_("Abandoned ?"), default=False)

	def __str__(self):
		return self.reference

class CustomerInvoiceLinkedFile(models.Model):
	# 
	cutomer_invoice    = models.ForeignKey(CustomerInvoice, verbose_name=_("Customer invoice"), null=True, on_delete=models.CASCADE)
	filename           = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	link       		   = models.URLField(_("Link"), blank=True, max_length=900)
	timestamp 		   = models.DateField(_("Timestamp"), blank=True)
	save_original_name = models.BooleanField(_("Save with original file name"), default=False, help_text=_("Save file on server with name 'PR##############-Original filename' (otherwise 'Original filename')"))

	def __str__(self):
		return self.filename

class CustomerInvoiceAttachedFile(models.Model):
	# 
	cutomer_invoice   = models.ForeignKey(CustomerInvoice, verbose_name=_("Customer invoice"), null=True, on_delete=models.CASCADE)
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The name of the file"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	timestamp 		  = models.DateField(_("Timestamp"), blank=True)

	def __str__(self):
		return self.filename

class CustomerInvoiceLine(models.Model):
	# 
	cutomer_invoice   = models.ForeignKey(CustomerInvoice, verbose_name=_("Customer invoice"), null=True, on_delete=models.CASCADE)
	line_type 		  = models.ForeignKey(LineType, verbose_name=_("Type"), null=True, on_delete=models.CASCADE)
	description       = models.TextField(_("Description"), blank=False, null=False)
	sku		          = models.CharField(_("Customer SKU"), max_length=200, blank=True)
	sales_tax 		  = models.IntegerField(_("Sales tax"), blank=False)
	unit_price_tax_excl = models.IntegerField(_("Unit price (net)"))
	unit_price_tax_incl = models.IntegerField(_("Unit price (Tax incl.)"))
	discount 		  = models.IntegerField(_("Discount"), blank=True, default=0)
	quantity 		  = models.IntegerField(_("Qty"), blank=False, default=1)

	def __str__(self):
		return self.description

class CustomerInvoiceContactType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

	def __str__(self):
		return self.key

class CustomerInvoiceContact(models.Model):
	# 
	cutomer_invoice = models.ForeignKey(CustomerInvoice, verbose_name=_("Customer invoice"), null=True, on_delete=models.CASCADE)
	third_party  	= models.ForeignKey(ThirdParty, verbose_name=_("Third-party"), blank=True, null=True, on_delete=models.CASCADE)
	contact  		= models.ForeignKey(Contact, verbose_name=_("Users | Contacts/Addresses"), blank=True, null=True, on_delete=models.CASCADE)
	contact_type  	= models.ForeignKey(VendorInvoiceContactType, verbose_name=_("Users | Contacts/Addresses"), blank=True, null=True, on_delete=models.CASCADE, help_text=_("You can change values from this list from the Setup >> Dictionnaries"))

	def __str__(self):
		return self.contact