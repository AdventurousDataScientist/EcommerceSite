from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    post_date = models.DateField(default=datetime.today().date())
    sell_date = models.DateField(default=datetime(year=9999, month=12, day=31))
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_items", null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bought_items", null=True)

# Create your models here.
