from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('myaccount/', views.MyAccount, name='myaccount'),
    path('customerMyAccount', views.customerMyAccount, name='customerMyAccount'),
    path('vendorMyAccount', views.vendorMyAccount, name='vendorMyAccount'),
]
