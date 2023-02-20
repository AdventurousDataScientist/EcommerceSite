# Generated by Django 4.1.1 on 2023-02-14 01:04

import creditcards.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_item_name_alter_item_post_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('credit_card_number', creditcards.models.CardNumberField(max_length=25, verbose_name='credit_card_number')),
                ('expiration_date', creditcards.models.CardExpiryField(verbose_name='expiration_date')),
                ('cvv', creditcards.models.SecurityCodeField(max_length=4, verbose_name='cvv')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='post_date',
            field=models.DateField(default=datetime.date(2023, 2, 13)),
        ),
    ]
