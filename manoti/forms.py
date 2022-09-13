from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from .utils import generate_customer_code, generate_vendor_code


# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from .models import ThirdParty, Contact


class ThirdPartyForm(forms.ModelForm):

	customer_code = forms.CharField(max_length=1000, label=_('Customer code'), initial=generate_customer_code(), widget=forms.TextInput(attrs={'class':'form-control'}))
	vendor_code   = forms.CharField(max_length=1000, label=_('Vendor code'), initial=generate_vendor_code(), widget=forms.TextInput(attrs={'class':'form-control'}))
	class Meta:
		model = ThirdParty
		exclude = [
			'date_added',
			'customer_code_number',
			'vendor_code_number'
		]