"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('employees/', include('employees.urls')),
    path('products/', include('products.urls')),

    path('inventories/', include('inventories.urls')),
    path('purchases/', include('purchases.urls')),
    path('sales/', include('sales.urls')),

    # path('approvers/', include('approvers.urls')),



    path('analyses/', include('analyses.urls')),

    path('api/', include('apis.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('profile/', user_views.profile, name='profile'),
    path('profile/password/', user_views.change_password, name='change_password'),

    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomLoginForm),
        name='login'),

    # Include Django auth URLs for login/logout
    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('pages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
