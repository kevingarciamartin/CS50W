# Generated by Django 4.2.3 on 2023-08-01 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_imageurl_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listings',
        ),
        migrations.AddField(
            model_name='listing',
            name='lister',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
