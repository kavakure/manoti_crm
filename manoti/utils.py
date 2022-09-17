from .models import ThirdParty, Contact, Proposal
from datetime import datetime

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

	pro_ref_arr = []
	proposals = Proposal.objects.all()
	prop = Proposal.objects.filter(is_validated=True).order_by('timestamp').first()
	if prop == None:
		validated_number = 1
	else:
		validated_number = prop.reference_number+1

	for prop in proposals:
		pro_ref_arr.append(prop.reference_number)

	if len(pro_ref_arr) == 0:
		draft_number = 1
	else:
		draft_number = max(pro_ref_arr)+1

	codes = {
		'draft_number': draft_number,
		'validated_number' : validated_number,
	}
	return codes
