from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.seller_index, name="seller_index"),
    path('register/', views.register, name="seller_register"),
    path('otp/', views.otp, name="seller_otp"),
    path('login/', views.login, name="seller_login"),
    path('logout/', views.logout, name="seller_logout"),
    path('add_product/', views.add_product, name="add_product"),
    path('edit_seller/', views.edit_seller_profile, name='edit_seller')

]