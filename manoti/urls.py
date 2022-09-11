from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dahshboard, name='dashboard'),
    url(r'^third-parties/$', views.third_party_homepage, name='third_party_homepage'),
    url(r'^third-party-list/$', views.list_third_parties, name='list_third_parties'),
    url(r'^third-party-list-filtered/(?P<thirdparty_type>[-\w]+)/$', views.filtered_list_third_parties, name='filtered_list_third_parties'),
    url(r'^third-party-view/(?P<thirdparty_id>[-\w]+)/$', views.third_party_view, name='third_party_view'),
    url(r'^contact-list/$', views.list_contacts, name='list_contacts'),
    url(r'^contact_list-filtered/(?P<thirdparty_type>[-\w]+)/$', views.filtered_list_contact, name='filtered_list_contact'),
    url(r'^contact-view/(?P<contact_id>[-\w]+)/$', views.contact_view, name='contact_view'),
]