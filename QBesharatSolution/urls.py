"""QBesharatSolution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from QBesharat import views
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from QBesharatSolution.views import start_support, stop_support

admin.site.site_header = _('QBesharat Administration Site')
admin.site.site_title = _('Welcome to QBesharat administration control panel')

urlpatterns = [
    path('', lambda request: redirect('/fa/admin/', permanent=False)),
]

urlpatterns += i18n_patterns(
    path('summernote/', include('django_summernote.urls')),
    path('admin/start_support/', start_support, name='start_support'),
    path('admin/stop_support/', stop_support, name='stop_support'),
    path('admin/', admin.site.urls),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
