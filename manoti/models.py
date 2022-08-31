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