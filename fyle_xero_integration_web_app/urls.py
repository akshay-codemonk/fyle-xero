"""fyle_xero_integration_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from decorator_include import decorator_include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from apps.user.views import UserLoginView
from apps.xero_workspace.decorators import is_workspace_user
from fyle_xero_integration_web_app import settings

urlpatterns = [path('admin/', admin.site.urls),
               path('accounts/', include('allauth.urls')),
               path('', UserLoginView.as_view(), name='home'),
               path('workspace/',
                    decorator_include([login_required, is_workspace_user],
                                      ('apps.xero_workspace.urls', 'xero_workspace'))),
               path('workspace_jobs/', include('apps.xero_workspace.job_urls'))
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
