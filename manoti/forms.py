from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

from .utils import generate_third_party_codes


# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from .models import ThirdParty, Contact, Proposal, PurchaseOrder, ProposalLine


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

		]

		widgets = {
			'timestamp': DateTimeInput(),
			'delivery_date': DateInput(),
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