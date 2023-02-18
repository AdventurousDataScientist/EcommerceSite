from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, BaseUserManager, AbstractUser
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    post_date = models.DateField(default=datetime.today().date())
    sell_date = models.DateField(default=datetime(year=9999, month=12, day=31))
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_items", null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bought_items", null=True)

class PaymentModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    credit_card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f'username: {self.user.get_username()}, Credit_Card_Number: {self.credit_card_number}'

class Profile(models.Model): # user is the parent
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)

    def __str__(self):
        return f'username: {self.user.get_username()}, Balance: {self.balance}'