# Generated by Django 3.1.2 on 2020-11-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20201123_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
