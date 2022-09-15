from django.contrib import admin

from manoti.models import *


class ThirdPartyOptions(admin.ModelAdmin):
	list_display = ('name', 'customer_code', 'customer_code_number', 'vendor_code', 'vendor_code_number', 'is_vendor')

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
admin.site.register(Proposal)
admin.site.register(PurchaseOrder)

admin.site.register(BankAccount)
admin.site.register(VendorInvoice)
admin.site.register(CustomerInvoice)
admin.site.register(StatusChoices)
