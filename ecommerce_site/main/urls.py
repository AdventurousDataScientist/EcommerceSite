from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("create", views.create, name="create"),
    path("item/<int:id>", views.show_item, name="show_item"),
    path("inventory", views.list_all_items, name="inventory"),
    path("cart", views.cart, name="cart")
]