from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User, BaseUserManager, AbstractUser
# from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # one user can have many stores
    name = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=200)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000, default='')
    
    def __str__(self):
        return f"{self.owner.username}'s store: {self.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # one user can have many orders
    store = models.ForeignKey(Store, on_delete=models.CASCADE) # one user can have many orders

    def __str__(self):
        return f'Order for {self.user.username} from store: {self.store.name}'

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.TextField(max_length=100, null=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.TextField(max_length=1000, null=True)
    post_date = models.DateField(default=date.today())
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f'Item: {self.name}, Price: {self.price}, Store: {self.store}'


class PurchasedItem(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=datetime(year=9999, month=12, day=31))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'order: {self.order}, Item: {self.name}, price: {self.price}, quantity: {self.quantity}, order date: {self.purchase_date}'


class Profile(models.Model): # user is the parent
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    credit_card_number = models.CharField(max_length=16, default='1111111111111111')
    expiration_date = models.CharField(max_length=5, default='11111')
    cvv = models.CharField(max_length=3, default='111')

    def __str__(self):
        return f'username: {self.user.get_username()}, Balance: {self.balance}, Credit Card Number: {self.credit_card_number}'
    






