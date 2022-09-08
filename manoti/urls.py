from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dahshboard, name='dashboard'),
    url(r'^third-parties/$', views.third_party_homepage, name='third_party_homepage'),
    url(r'^third-party-list/$', views.list_third_parties, name='list_third_parties'),
]