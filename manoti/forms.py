from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from .utils import generate_third_party_codes


# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from .models import ThirdParty, Contact


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