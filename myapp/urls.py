from django.urls import path
from . import views

urlpatterns = [
    path('', views.aircraft_list, name='aircraft_list'),
    path('aircraft/', views.aircraft_list, name='aircraft_list'),
    path('dashboard/', views.aircraft_list, name='dashboard'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('sign-in/', views.signin_view, name='sign-in'),
    path('sign-up/', views.signup_view, name='sign-up'),
    path('rtl/', views.prevision_view, name='rtl'),
    path('profile/', views.prevision_view, name='profile'),
    path('receive_data/', views.receive_data, name='receive_data'),
    path('receive_DeliveryOrders/', views.receive_deliveryorders, name='receive_DeliveryOrders'),



]
