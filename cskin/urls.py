import views
import settings

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^healthCheck', views.healthCheck),
    url(r'^seeImages', views.seeImages),
    url(r'^login', views.loginView),
    url(r'^processLogin', views.processLogin),
    url(r'^processLogout', views.processLogout),
    url(r'^processImageUpload', views.processImageUpload),
    url(r'^testUploadImage', views.testUploadImage),
    url(r'^getPatientImages', views.getPatientImages),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
