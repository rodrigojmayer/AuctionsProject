# Generated by Django 3.1.2 on 2020-11-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auctionlistings_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='image',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
