"""
URL configuration for spotify project.

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
from django.urls import path
from api.views import *
from api.views import ClerkAuthCallback
from api.middlewares import ProtectRouteMiddleware, RequireAdminMiddleware
from django.utils.decorators import decorator_from_middleware

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/callback", ClerkAuthCallback.as_view()),
    path('albums/', get_all_albums),
    path('albums/<int:id>/', get_album_by_id),
    path('users/', get_all_users),
    path('admin/check/', CheckAdminView.as_view()),
]
