# Generated by Django 4.2.3 on 2023-08-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='imageURL',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
