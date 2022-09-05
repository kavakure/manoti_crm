from django.core.exceptions import ValidationError
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

import os
from django.core.exceptions import ValidationError
	
def validate_file_size(value):
	filesize = value.size
	
	if filesize > 2097152:
		raise ValidationError(_('The maximum file size that can be uploaded is 2MB'))
	else:
		return value

def validate_image_file_extension(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = ['.jpg', '.png']
	if not ext.lower() in valid_extensions:
		raise ValidationError(_('Sorry! Only .jpg or .png images are accepted'))

def validate_document_file_extension(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
	if not ext.lower() in valid_extensions:
		raise ValidationError(_('Sorry: Unsupported file! Only .pdf, .doc, .docx, .jpg, .png, .xlsx, .xls files are accepted'))