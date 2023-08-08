# Generated by Django 4.2.3 on 2023-08-03 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_rename_highest_bidder_bid_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='number_of_bids',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='highest_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest_bid', to='auctions.bid'),
        ),
    ]
