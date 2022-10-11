from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

from .utils import generate_third_party_codes


# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from .models import ThirdParty, Contact, Proposal, PurchaseOrder, ProposalLine, ProposalLinkedFile, ProposalAttachedFile, BankAccount
from .models import BankAccountAttachedFile, BankAccountLinkedFile, BankEntry, BankEntryAttachedFile, VendorInvoiceLinkedFile, VendorInvoiceAttachedFile, VendorInvoice, VendorInvoiceLine


class ThirdPartyForm(forms.ModelForm):
	"""Form used to create or edit a Third Party"""
	customer_code = forms.CharField(max_length=1000, label=_('Customer code'), initial=generate_third_party_codes()['customer_code'], widget=forms.TextInput(attrs={'class':'form-control'}))
	vendor_code   = forms.CharField(max_length=1000, label=_('Vendor code'), initial=generate_third_party_codes()['vendor_code'], widget=forms.TextInput(attrs={'class':'form-control'}))
	vendor_code_number  = forms.IntegerField(label=_('Vendor code number'), initial=generate_third_party_codes()['vendor_code_number'], widget=forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}))
	customer_code_number = forms.IntegerField(label=_('Customer code number'), initial=generate_third_party_codes()['customer_code_number'], widget=forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}))
	class Meta:
		model = ThirdParty
		exclude = [
			'date_added'
		]

class ContactForm(forms.ModelForm):
	"""Form used to create or edit a Contact"""
	class Meta:
		model = Contact
		exclude = [
			'date_added'
		]

class DateTimeInput(forms.DateTimeInput):
	input_type = 'datetime-local'

class DateInput(forms.DateInput):
	input_type = 'date'

class ProposalForm(forms.ModelForm):
	"""Form used to create or edit a commercial proposal"""

	class Meta:
		model = Proposal

		exclude = [
			'shipping_metod',
			'author',
			'reference',
			'reference_number',
			'amount_excl_tax',
			'tax',
			'amount_incl_tax',
			'is_validated',
			'is_signed',
			'is_billed',
		]

		widgets = {
			'timestamp': DateTimeInput(attrs={'style': 'width: 200px'}),
			'delivery_date': DateInput(attrs={'style': 'width: 200px'}),
		}

class ProposalLineForm(forms.ModelForm):
	"""Form used to create or edit a commercial proposal"""
	sales_tax = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 80px', 'class':'form-control'}))

	class Meta:
		model = ProposalLine
		widgets = {
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'sales_tax': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'unit_price': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px', 'placeholder':'XXX'}),
			 'discount': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'total_tax_excl': forms.NumberInput(attrs={'style': 'width: 80px'}),
			}
		exclude = [
			'proposal',
			'total_tax_incl',
			
		]

class ProposalStatusForm(forms.ModelForm):
	"""Form used to set the status of an commercial proposal to determine if it was accepted or not by the customer"""

	class Meta:
		model = Proposal
		fields = ['is_signed']


class ProposalLinkedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a commercial proposal"""

	class Meta:
		model = ProposalLinkedFile
		fields = ['proposal', 'label', 'link'] 


class ProposalAttachedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a commercial proposal"""

	class Meta:
		model = ProposalAttachedFile
		fields = ['proposal', 'filename', 'attachment'] 

class BankAccountForm(forms.ModelForm):
	"""Form used to create a financial institution"""

	class Meta:
		model = BankAccount

		exclude = [
			'author',
			'balance',
			'entries_to_reconcile',
			'entries_late_to_reconcile',
		]
		widgets = {
			'timestamp': DateInput(attrs={'style': 'width: 200px'}),
		}

class BankAccountEditForm(forms.ModelForm):
	"""Form used to edit a financial institution"""

	class Meta:
		model = BankAccount

		exclude = [
			'author',
			'balance',
			'entries_to_reconcile',
			'entries_late_to_reconcile',
			'initial_balance',
			'timestamp',
		]
		widgets = {
			'timestamp': DateInput(),
		}

class BankAccountLinkedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a bank account"""

	class Meta:
		model = BankAccountLinkedFile
		fields = ['bank', 'label', 'link'] 


class BankAccountAttachedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a bank account"""

	class Meta:
		model = BankAccountAttachedFile
		fields = ['bank', 'filename', 'attachment'] 

class BankEntryForm(forms.ModelForm):
	"""Form used to add an entry to a financial institution"""
	amount = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))

	class Meta:
		model = BankEntry

		fields = ['date', 'value_date', 'label', 'amount', 'bank', 'payment_type', 'check_transfer_number', 'check_transfer_sender', 'bank_of_check', 'accounting_account', 'subledger_account']

		widgets = {
			'date': DateTimeInput(attrs={'style': 'width: 200px'}), 
			'value_date': DateTimeInput(attrs={'style': 'width: 200px'}), 
			'label': forms.TextInput(attrs={'rows': '3'}), 
		}

class BankEntryAttachedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a bank entry"""

	class Meta:
		model = BankEntryAttachedFile
		fields = ['entry', 'filename', 'attachment'] 

class VendorInvoiceLinkedFileForm(forms.ModelForm): 
	"""Form used to add a linked file to a Vendor Invoice"""

	class Meta:
		model = VendorInvoiceLinkedFile
		fields = ['vendor_invoice', 'filename', 'link'] 


class VendorInvoiceAttachedFileForm(forms.ModelForm):
	"""Form used to add a linked file to a Vendor Invoice"""

	class Meta:
		model = VendorInvoiceAttachedFile
		fields = ['vendor_invoice', 'filename', 'attachment'] 

class VendorInvoiceForm(forms.ModelForm):
	"""Form used to create or edit a commercial proposal"""

	class Meta:
		model = VendorInvoice

		exclude = [
			'author',
			'reference',
			'reference_number',
			'total_tax_excl',
			'tax_amount',
			'total_tax_incl',
			'is_validated',
			'is_abandoned',
			'is_paid',
			'total_payment',
			'remaining_unpaid',
		]

		widgets = {
			'date': DateTimeInput(attrs={'style': 'width: 200px'}),
			'payment_due': DateInput(attrs={'style': 'width: 200px'}),
		}

class VendorInvoiceLineForm(forms.ModelForm):
	"""Form used to add or edit a line of a vendor invoice"""
	sales_tax = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'style': 'width: 80px', 'class':'form-control'}))

	class Meta:
		model = VendorInvoiceLine
		widgets = {
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'sku': forms.TextInput(attrs={'style': 'width: 90px'}),
			 'sales_tax': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'unit_price_tax_excl': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'unit_price_tax_incl': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px', 'placeholder':'XXX'}),
			 'discount': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'quantity': forms.NumberInput(attrs={'style': 'width: 80px'}),
			 'total_tax_excl': forms.NumberInput(attrs={'style': 'width: 80px'}),
			}
		exclude = [
			'vendor_invoice',
			'total_tax_incl',
			'total_tax_excl',
			'remaining_unpaid',
			
		]