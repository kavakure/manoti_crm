from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from .validators import validate_file_size, validate_image_file_extension, validate_document_file_extension

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


class Business(models.Model):
	user                = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, help_text=_("The user object that owns Company/Organization"))
	name                = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The full name of your Company/Organization"))
	address             = models.TextField(_("Full Address"), blank=True, null=True, help_text=_("Please mention here the full address of your Company/Organization"))
	address             = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the Company/Organization"))
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
	capital             = models.IntegerField(_("Capital"))
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

	user              = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, help_text=_("The user object related to the employee"))
	last_name         = models.CharField(_("Last name"), max_length=200, blank=True)
	first_name        = models.CharField(_("First name"), max_length=200, blank=True)
	username          = models.CharField(_("Frist name"), max_length=200, blank=True, unique=True)
	is_administrator  = models.BooleanField(_("Administrator ?"), default=False)
	is_employee 	  = models.BooleanField(_("Employee"), default=True)
	# supervisor        = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Supervisor"))
	# force_expense_report_validator = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Force expense report validator"))
	# force_leave_request_validator = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Force leave request validator"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of the employee"))
	city              = models.CharField(_("City"), max_length=200, blank=True, default="Bujumbura", help_text=_("Indicate the city ot town address of the employee"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where the employee is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where your the employee lives"))
	mobile_phone      = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of the employee"))
	business_phone    = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of the employee"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of your Company/Organization"))
	note              = models.TextField(_("Notes"), blank=True, null=True, help_text=_("Any additional note or information about the employee"))
	signature         = models.TextField(_("Signature"), blank=True, null=True)

	job_postion       = models.CharField(_("Job position"), blank=True, null=True, max_length=30)
	average_hourly_rate = models.IntegerField(_("Average hourly rate"))
	average_daily_rate  = models.IntegerField(_("Average Daily rate"))
	salary     		  = models.IntegerField(_("Salary"))
	hours_worked_per_week = models.IntegerField(_("Hours worked (per week)"))
	employement_start = models.DateField(_("Employement date begun"), blank=True, help_text=_("Ex: 01/04/2019, The date when The employee started working for the company"))
	employement_end   = models.DateField(_("Employement date ended"), blank=True, help_text=_("Ex: 01/04/2019, The date when The employee left the company"))
	date_of_birth 	  = models.DateField(_("Date of birth"), blank=True, )


# Customer Relationship Management (CRM)
	
class PhoneNumber(models.Model):
	type              = models.CharField(_("Third party name"), max_length=200, blank=True, default="Mobile", help_text=_("The type of the phone device"))
	phone_number	  = models.CharField(_("Phone Number"), blank=False, max_length=30,)

class BusinessEntityType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class ThirdPartyType(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class ThirdParty(models.Model):
	# Companies and contacts management (customers, vendors and prospects, ...)
	business          = models.ForeignKey(Business, blank=False, null=False, on_delete=models.CASCADE)
	name              = models.CharField(_("Third party name"), max_length=200, blank=True, help_text=_("The full name of the Third Party"))
	alias_name        = models.CharField(_("Alias name (commercial, trademark, ...)"), max_length=200, blank=True, help_text=_("The Alias name used for other purposes"))
	prospect_customer = models.CharField(_("Prospect / Customer"), choices=PROSPOECT_CUSTOMER_CHOICES, max_length=200, blank=True, help_text=_("Defines which type the thirdparty is"))
	customer_code     = models.CharField(_("Customer code"), max_length=200, blank=True)
	vendor_code       = models.CharField(_("Vendor code"), max_length=200, blank=True)
	status 			  = models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=200, blank=True)
	address           = models.TextField(_("Google Map URL"), blank=True, null=True, help_text=_("Google Map URL of the Company/Organization"))
	po_box	          = models.CharField(_("P.O. Box"), max_length=200, blank=True, null=True, help_text=_("Please mention the postal office box of your Company/Organization"))
	town              = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("Indicate the town address of your Company/Organization"))
	country           = models.CharField(_("Country"), max_length=200, blank=True, default ="Burundi", help_text=_("Indicate the country where your Company/Organization is located and/or registered"))
	state_province    = models.CharField(_("State/Province"), max_length=200, blank=True, default ="Bujumbura", help_text=_("Indicate the State or Province where your Company/Organization is located and/or registered"))
	phone             = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30, help_text=_("The Phone number of your Company/Organization"))
	email             = models.EmailField(_("Email"), blank=True, max_length=255, help_text=_("The email address of your Company/Organization"))
	website           = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("The website of your Company/Organization"))
	professional_id_1 = models.CharField(_("Professional ID 1"), max_length=200, blank=True, null=True)
	professional_id_2 = models.CharField(_("Professional ID 2"), max_length=200, blank=True, null=True)
	professional_id_3 = models.CharField(_("Professional ID 3"), max_length=200, blank=True, null=True)
	professional_id_4 = models.CharField(_("Professional ID 4"), max_length=200, blank=True, null=True)
	professional_id_5 = models.CharField(_("Professional ID 5"), max_length=200, blank=True, null=True)
	professional_id_6 = models.CharField(_("Professional ID 6"), max_length=200, blank=True, null=True)
	vat_id            = models.CharField(_("VAT ID"), max_length=200, blank=True, null=True)
	registre_de_commerce = models.CharField(_("Registre de Commerce"), max_length=200, blank=True, null=True)
	sales_tax_is_used = models.BooleanField(_("Are Sales tax used by your Company/Organization?"), default=False)
	third_party_type  = models.ForeignKey(ThirdPartyType, verbose_name=_("Third-party type"), blank=True, null=True, on_delete=models.CASCADE)
	business_entity_type = models.ForeignKey(BusinessEntityType, verbose_name=_("Business entity type"), blank=True, null=True, on_delete=models.CASCADE)
	workforce		  = models.IntegerField(_("workforce"), blank=True, default=1)
	capital           = models.IntegerField(_("Capital"))
	assigned_representative = models.ForeignKey(Employee, verbose_name=_("Business entity type"), null=True, on_delete=models.CASCADE)
	logo              = models.FileField(_("Logo"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG, will be used on various documents related to your Company/Organization"))

class Title(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class Contact(models.Model):
	#
	third_party 	  = models.ForeignKey(ThirdParty, verbose_name=_("Third party"), null=True, on_delete=models.CASCADE)
	name              = models.CharField(_("Last name / Label"), max_length=200, blank=True)
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

class PaymentMethod(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class PaymentTerms(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class Source(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class AvailabilityDelay(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class ShippingMetod(models.Model):
	# 
	key      		 = models.CharField(_("Key"), max_length=200, blank=False, null=False)
	value      		 = models.CharField(_("Value"), max_length=200, blank=False, null=False)

class ProposalDocumentTemplate(models.Model):
	# 
	filename          = models.CharField(_("Name"), max_length=200, blank=True, help_text=_("The full name of your Company/Organization"))
	attachment        = models.FileField(_("File attached"), upload_to='media/uploads', blank=True, validators=[validate_file_size,])
	description       = models.TextField(_("Description"), blank=True, null=True)
	content        	  = models.TextField(_("Content of the document"), blank=True, null=True)

class Proposal(models.Model):
	# 
	reference      	= models.CharField(_("Reference"), max_length=200, blank=False, null=False, default="Draft")
	customer_reference= models.CharField(_("Customer reference"), max_length=200, blank=True, null=True)
	customer 	  	= models.ForeignKey(ThirdParty, verbose_name=_("Third party"), null=True, on_delete=models.CASCADE)
	timestamp 		= models.DateField(_("Date of birth"), blank=True)
	validity_duration = models.IntegerField(_("Validity duration"), help_text=_("days"))
	payment_terms 	= models.ForeignKey(PaymentTerms, verbose_name=_("Payment terms"), null=True, on_delete=models.CASCADE)
	payment_method 	= models.ForeignKey(PaymentMethod, verbose_name=_("Payment method"), null=True, on_delete=models.CASCADE)
	source 	  		= models.ForeignKey(Source, verbose_name=_("Source"), null=True, on_delete=models.CASCADE)
	availability_delay = models.ForeignKey(AvailabilityDelay, verbose_name=_("Availability delay (after order)"), null=True, on_delete=models.CASCADE)
	shipping_metod	= models.ForeignKey(ShippingMetod, verbose_name=_("Shipping Method"), null=True, on_delete=models.CASCADE)
	delivery_date	= models.DateField(_("Delivery date"), blank=True)
	document_template = models.ForeignKey(ProposalDocumentTemplate, verbose_name=_("Default doc template"), null=True, on_delete=models.CASCADE)
	note_private    = models.TextField(_("Private note"), blank=True, null=True)
	note_public     = models.TextField(_("Public Note"), blank=True, null=True)
	#The money figures
	amount_excl_tax = models.IntegerField(_("Amount (excl. tax)"))
	tax = models.IntegerField(_("Amount tax"))
	amount_incl_tax = models.IntegerField(_("Amount (inc. tax)"))
	