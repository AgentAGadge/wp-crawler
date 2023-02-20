"""wp_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

_admin_site_get_urls = admin.site.get_urls

def get_urls():        
    from django.conf.urls import url
    urls = _admin_site_get_urls()
    urls += [
            url(r'^my_custom_view/$',
                 admin.site.admin_view(MyCustomView.as_view()))
        ]
    return urls

admin.site.get_urls = get_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hyperlist/", include('hyperlist.urls')),
]
