from .models import ThirdParty, Contact, Proposal, VendorInvoice
from datetime import datetime

#Imports for pdf generation
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context, loader
from django.http import HttpResponse
# from cgi import escape

def generate_third_party_codes():

	ven = ThirdParty.objects.all().order_by('-vendor_code_number').first()
	cus = ThirdParty.objects.all().order_by('-customer_code_number').first()
	if ven == None:
		ven_number = 1
	else:
		ven_number = ven.vendor_code_number+1

	if cus == None:
		cus_number = 1
	else:
		cus_number = cus.customer_code_number+1

	cus_code = "CU%s-%s" % (datetime.now().strftime("%y%m"), str(cus_number).zfill(3))
	ven_code = "SU%s-%s" % (datetime.now().strftime("%y%m"), str(ven_number).zfill(3))

	codes = {
		'vendor_code_number': ven_number,
		'customer_code_number' : cus_number,
		'customer_code' : cus_code,
		'vendor_code' : ven_code,
	}
	return codes

def generate_proposal_reference():

	all_proposals = Proposal.objects.all().order_by('-timestamp').first()
	validated_proposals = Proposal.objects.filter(is_validated=True).order_by('-timestamp').first()
	if validated_proposals == None:
		validated_number = 1
	else:
		validated_number = validated_proposals.reference_number+1

	if all_proposals == None:
		draft_number = 1
	else:
		draft_number = all_proposals.reference_number+1

	codes = {
		'draft_number': draft_number,
		'validated_number' : validated_number,
	}
	return codes


def generate_vendor_invoice_reference():

	invoices = VendorInvoice.objects.all().order_by('-date').first()
	validated_invoices = VendorInvoice.objects.filter(is_validated=True).order_by('-date').first()
	if validated_invoices == None:
		validated_number = 1
	else:
		validated_number = validated_invoices.reference_number+1

	if invoices == None:
		draft_number = 1
	else:
		draft_number = invoices.reference_number+1

	codes = {
		'draft_number': draft_number,
		'validated_number' : validated_number,
	}
	return codes

def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None