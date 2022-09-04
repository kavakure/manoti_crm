from django.contrib import admin

from manoti.models import *

admin.site.register(Business)
admin.site.register(BusinessAccountant)
admin.site.register(SocialNetwork)
admin.site.register(Employee)
admin.site.register(BusinessEntityType)
admin.site.register(ThirdPartyType)
admin.site.register(ThirdParty)
admin.site.register(Title)
admin.site.register(Contact)
admin.site.register(PaymentType)
admin.site.register(PaymentTerms)
admin.site.register(Source)
admin.site.register(AvailabilityDelay)
admin.site.register(ShippingMetod)
admin.site.register(ProposalDocumentTemplate)
admin.site.register(Proposal)

admin.site.register(BankAccount)
admin.site.register(VendorInvoice)
admin.site.register(CustomerInvoice)
