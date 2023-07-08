from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("create", views.create, name="create"),
    path("item/<int:id>", views.show_item, name="show_item"),
    path("inventory", views.list_all_items, name="inventory"),
    path("cart", views.cart, name="cart"),
    path("account", views.account, name="account"),
    path("history", views.history, name="history"),
    path("checkout", views.checkout, name="checkout"),
    path("balance", views.balance, name="balance"),
    path("end", views.end, name="end"),
    path("create_store", views.create_store, name="create_store"),
    path("store/<str:username>/<int:store_id>", views.show_store, name="show_store"),
]