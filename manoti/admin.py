from django.contrib import admin

from manoti.models import *


class ThirdPartyOptions(admin.ModelAdmin):
	list_display = ('name', 'customer_code', 'customer_code_number', 'vendor_code', 'vendor_code_number', 'is_vendor')

class  ProposalLine_Inline(admin.StackedInline):
	model = ProposalLine
	extra = 2

class  ProposalLinkedFile_Inline(admin.StackedInline):
	model = ProposalLinkedFile
	extra = 2

class  ProposalAttachedFile_Inline(admin.StackedInline):
	model = ProposalAttachedFile
	extra = 2

class ProposalOptions(admin.ModelAdmin):
	list_display = ('reference', 'customer_reference', 'third_party', 'timestamp', 'amount_incl_tax', 'is_validated', 'is_signed', 'is_billed')
	inlines = [ProposalLine_Inline, ProposalLinkedFile_Inline, ProposalAttachedFile_Inline]

class  VendorInvoiceAttachedFile_Inline(admin.StackedInline):
	model = VendorInvoiceAttachedFile
	extra = 2

class  VendorInvoiceLine_Inline(admin.StackedInline):
	model = VendorInvoiceLine
	extra = 2

class VendorInvoiceOptions(admin.ModelAdmin):
	list_display = ('reference', 'vendor_reference', 'third_party', 'date', 'total_tax_excl', 'is_validated', 'is_paid', 'is_abandoned')
	inlines = [VendorInvoiceLine_Inline, VendorInvoiceAttachedFile_Inline]

admin.site.register(Business)
admin.site.register(BusinessAccountant)
admin.site.register(SocialNetwork)
admin.site.register(Employee)
admin.site.register(BusinessEntityType)
admin.site.register(ThirdPartyType)
admin.site.register(ThirdParty, ThirdPartyOptions)
admin.site.register(Title)
admin.site.register(Contact)
admin.site.register(PaymentType)
admin.site.register(PaymentTerms)
admin.site.register(Source)
admin.site.register(AvailabilityDelay)
admin.site.register(ShippingMetod)
admin.site.register(ProposalDocumentTemplate)
admin.site.register(Proposal, ProposalOptions)
admin.site.register(PurchaseOrder)

admin.site.register(BankAccount)
admin.site.register(BankEntry)
admin.site.register(BankAccountLinkedFile)
admin.site.register(BankAccountAttachedFile)

admin.site.register(LineType)
admin.site.register(VendorInvoice, VendorInvoiceOptions)
admin.site.register(CustomerInvoice)
admin.site.register(StatusChoices)
admin.site.register(Payment)
