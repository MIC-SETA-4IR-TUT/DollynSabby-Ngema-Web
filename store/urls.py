from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.main, name="home"),
    path('shop/', views.shop, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('store/', views.storemain, name="storemain"),
]
