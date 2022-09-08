from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from hello import views, urls
from manoti import views, urls

admin.autodiscover()

urlpatterns = [
    url(r'^/', include('hello.urls')),
    url(r'^crm/', include('manoti.urls')),
    path("admin/", admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
