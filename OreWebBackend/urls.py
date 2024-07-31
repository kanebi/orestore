"""
URL configuration for OreWebBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('allauth.urls'))
]

# return home single page app view on 404 not found error
handler404 = TemplateView.as_view(template_name='index.html')

# customizing the admin panel
admin.site.site_header = 'Ore Restaurant Admin'
admin.site.index_title = 'Welcome to Ore Restaurant Admin Panel'
admin.site.site_title = 'Ore Restaurant Admin Panel'
