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
	#Commerce related views
	url(r'^commerce/$', views.commerce_homepage, name='commerce_homepage'),
	url(r'^proposal-list/$', views.proposal_list, name='proposal_list'),
	url(r'^proposal-view/(?P<proposal_id>[-\w]+)/$', views.proposal_view, name='proposal_view'),
]