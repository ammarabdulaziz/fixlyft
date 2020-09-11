"""fixlyft_project URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from staffs.views import all_pickups, UpdatePickup
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('fixlyftadminff/', admin.site.urls),
    path('', include('fixlyft.urls')),
    path('allpickups/', all_pickups, name='allpickups'),
    path('<int:pk>/update/', UpdatePickup.as_view(), name='update'),
    path('stafflogout/', auth_views.LogoutView.as_view(template_name='staffs/logout.html'), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
