from django.urls import path, include
from .import views
from .otp import phone_validation, validate_otp
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/schedule-pickup/', views.SchedulePickup.as_view(), name='submit'),
    path('phonevalidation/', phone_validation, name='phone'),
    path('otpverification/', validate_otp, name='otp'),
    path('shops-schedule-pickup/', views.MobileShopSearch.as_view(), name='schedule'),
    path('shops/', views.shops, name='shops_table'),
    path('offers/', views.offers, name='offers'),
    path('delivery/', views.delivery, name='delivery'),
    path('support/', views.support, name='support'),
]
