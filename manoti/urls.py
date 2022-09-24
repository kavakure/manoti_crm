from django.conf.urls import url

from . import views

urlpatterns = [
	#Thirdparty related views
	url(r'^$', views.dahshboard, name='dashboard'),
	url(r'^third-parties/$', views.third_party_homepage, name='third_party_homepage'),
	url(r'^third-party-list/$', views.list_third_parties, name='list_third_parties'),
	url(r'^third-party-list-filtered/(?P<thirdparty_type>[-\w]+)/$', views.filtered_list_third_parties, name='filtered_list_third_parties'),
	url(r'^third-party-view/(?P<thirdparty_id>[-\w]+)/$', views.third_party_view, name='third_party_view'),
	url(r'^third-party-create/$', views.third_party_create, name='third_party_create'),
	url(r'^third-party-edit/(?P<thirdparty_id>[-\w]+)/$', views.third_party_edit, name='third_party_edit'),
	url(r'^third-party-delete/(?P<thirdparty_id>[-\w]+)/$', views.third_party_delete, name='third_party_delete'),
	url(r'^contact-list/$', views.list_contacts, name='list_contacts'),
	url(r'^contact_list-filtered/(?P<thirdparty_type>[-\w]+)/$', views.filtered_list_contact, name='filtered_list_contact'),
	url(r'^contact-view/(?P<contact_id>[-\w]+)/$', views.contact_view, name='contact_view'),
	url(r'^contact-delete/(?P<contact_id>[-\w]+)/$', views.contact_delete, name='contact_delete'),
	url(r'^contact-change-status/(?P<contact_id>[-\w]+)/$', views.contact_change_status, name='contact_change_status'),
	url(r'^contact-create/$', views.contact_create, name='contact_create'),
	url(r'^contact-edit/(?P<contact_id>[-\w]+)/$', views.contact_edit, name='contact_edit'),
	#Commerce related URLS
	url(r'^commerce/$', views.commerce_homepage, name='commerce_homepage'),
	url(r'^proposal-list/$', views.proposal_list, name='proposal_list'),
	url(r'^proposal-view/(?P<proposal_id>[-\w]+)/$', views.proposal_view, name='proposal_view'),
	url(r'^proposal-create/$', views.proposal_create, name='proposal_create'),
	url(r'^proposal-edit/(?P<proposal_id>[-\w]+)/$', views.proposal_edit, name='proposal_edit'),
	url(r'^proposal-delete/(?P<proposal_id>[-\w]+)/$', views.proposal_delete, name='proposal_delete'),
	url(r'^proposal-clone/(?P<proposal_id>[-\w]+)/$', views.proposal_clone, name='proposal_clone'),
	url(r'^proposal-set-status/(?P<proposal_id>[-\w]+)/$', views.proposal_set_status, name='proposal_set_status'),
	url(r'^proposal-toggle-validation/(?P<proposal_id>[-\w]+)/$', views.proposal_toggle_validation, name='proposal_toggle_validation'),
	url(r'^proposal-toggle-billing/(?P<proposal_id>[-\w]+)/$', views.proposal_toggle_billing_status, name='proposal_toggle_billing_status'),
	url(r'^proposal-line-add/(?P<proposal_id>[-\w]+)/$', views.proposal_line_add, name='proposal_line_add'),
	url(r'^proposal-line-delete/(?P<proposal_id>[-\w]+)/(?P<proposal_line_id>[-\w]+)/$', views.proposal_line_delete, name='proposal_line_delete'),
	url(r'^proposal-linked-file-add/(?P<proposal_id>[-\w]+)/$', views.proposal_linked_file_add, name='proposal_linked_file_add'),
	url(r'^proposal-linked-file-delete/(?P<proposal_id>[-\w]+)/(?P<linked_file_id>[-\w]+)/$', views.proposal_linked_file_delete, name='proposal_linked_file_delete'),
	url(r'^proposal-attached-file-add/(?P<proposal_id>[-\w]+)/$', views.proposal_attached_file_add, name='proposal_attached_file_add'),
	url(r'^proposal-attached-file-delete/(?P<proposal_id>[-\w]+)/(?P<attached_file_id>[-\w]+)/$', views.proposal_attached_file_delete, name='proposal_attached_file_delete'),
	#Billing area ralated URLS
	url(r'^billing/$', views.billing_homepage, name='billing_homepage'),
	#Bank|cash area related URLS
	url(r'^bank/$', views.bank_list, name='bank_list'),
	url(r'^bank-view/(?P<bank_id>[-\w]+)/$', views.bank_view, name='bank_view'),
	url(r'^bank-create/$', views.bank_create, name='bank_create'),
	url(r'^bank-edit/(?P<bank_id>[-\w]+)/$', views.bank_edit, name='bank_edit'),
	url(r'^bank-delete/(?P<bank_id>[-\w]+)/$', views.bank_delete, name='bank_delete'),
	url(r'^bank-linked-file-add/(?P<bank_id>[-\w]+)/$', views.bank_linked_file_add, name='bank_linked_file_add'),
	url(r'^bank-linked-file-delete/(?P<bank_id>[-\w]+)/(?P<linked_file_id>[-\w]+)/$', views.bank_linked_file_delete, name='bank_linked_file_delete'),
	url(r'^bank-attached-file-add/(?P<bank_id>[-\w]+)/$', views.bank_attached_file_add, name='bank_attached_file_add'),
	url(r'^bank-attached-file-delete/(?P<bank_id>[-\w]+)/(?P<attached_file_id>[-\w]+)/$', views.bank_attached_file_delete, name='bank_attached_file_delete'),
	url(r'^bank-entries/$', views.bank_entry_list, name='bank_entry_list'),
	url(r'^bank-entry-view/(?P<entry_id>[-\w]+)/$', views.bank_entry_view, name='bank_entry_view'),
	url(r'^bank-entry-create/$', views.bank_entry_create, name='bank_entry_create'),
]