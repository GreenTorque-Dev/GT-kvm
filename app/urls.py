from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("start/<str:domain_name>/", start_hypervisor, name="start_hypervisor"),

    path('', login_success, name='index'),
    path('index/', IndexPageView.as_view(), name='dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
