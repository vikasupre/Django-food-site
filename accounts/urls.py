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

    path('activate/<uidb64>/<token>', views.activate_account, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/<uidb64>/<token>',
         views.password_reset, name='password_reset'),
    path('password_reset_done/', views.password_reset_done,
         name='password_reset_done')

]
