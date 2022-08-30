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
    user                = models.ForeignKey(User, blank=False, null=True)
    name                = models.CharField(_("Name of the file attached"), max_length=200, blank=True, help_text=_("The user object that owns Company/Organization"))
    address             = models.TextField(_("Full Address"), blank=True, null=True, help_text=_("Please mention here the full address of your Company/Organization"))
    zip_code            = models.CharField(_("Zip"), max_length=200, blank=True, help_text=_("name of the file to attach to the CV Template"))
    town                = models.CharField(_("Town"), max_length=200, blank=True, help_text=_("name of the file to attach to the CV Template"))
    country             = models.CharField(_("Country"), max_length=200, blank=True, help_text=_("name of the file to attach to the CV Template"))
    state_province      = models.CharField(_("State/Province"), max_length=200, blank=True, help_text=_("name of the file to attach to the CV Template"))
    main_currency       = models.CharField(_("Main currency"), max_length=200, blank=True, help_text=_("name of the file to attach to the CV Template"))
    phone               = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30)
    email               = models.EmailField(_("Email"), blank=True, max_length=255)
    website             = models.URLField(_("Web"), blank=True, max_length=900, help_text=_("website of "))
    logo                = models.FileField(_("Logo"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG"))
    logo_squarred       = models.FileField(_("Logo (squarred)"), upload_to='media/uploads', blank=True, validators=[validate_file_size, validate_document_file_extension], help_text=_("PNG or JPEG"))
    address             = models.TextField(_("Notes"), blank=True, null=True, help_text=_("Any note about the Company/Organization"))
    
    # Company/Organization identities
    manager_name        = models.CharField(_("Manager(s) name (CEO, director, president...)"), max_length=200, blank=True, help_text=_("Manager(s) name (CEO, director, president...)"))
    data_protection_officer = models.CharField(_("Data Protection Officer (DPO, Data Privacy or GDPR contact)"), max_length=200, blank=True, help_text=_("TO-DO: edit this text"))
    capital             = models.IntegerField(_("Capital"))
    business_entity_type = models.CharField(_("Business entity type"), max_length=200, blank=True, null=True)
    professional_id_1   = models.CharField(_("Professional ID 1"), max_length=200, blank=True, null=True)
    professional_id_2   = models.CharField(_("Professional ID 2"), max_length=200, blank=True, null=True)
    professional_id_3   = models.CharField(_("Professional ID 3"), max_length=200, blank=True, null=True)
    professional_id_4   = models.CharField(_("Professional ID 4"), max_length=200, blank=True, null=True)
    professional_id_5   = models.CharField(_("Professional ID 5"), max_length=200, blank=True, null=True)
    professional_id_6   = models.CharField(_("Professional ID 6"), max_length=200, blank=True, null=True)
    vat_id              = models.CharField(_("VAT ID"), max_length=200, blank=True, null=True)
    object_of_the_company = models.TextField(_("Object of the company"), blank=True, null=True)
    
    # Fiscal Year
    object_of_the_company = models.CharField(_("Starting month of the fiscal year"), blank=False, null=False, choices=MONTH_CHOICES, default='1')

    # Type of sales tax
     sales_tax_is_used = models.BooleanField(_("Are Sales tax used ?"), default=False)
