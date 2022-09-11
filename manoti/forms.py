from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from .models import ThirdParty, Contact


class ThirdPartyForm(forms.ModelForm):
	class Meta:
		model = ThirdParty
		exclude = [
			'vendor_code_number',
			'customer_code_number',
			'date_added'
		]