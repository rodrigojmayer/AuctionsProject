# Generated by Django 3.1.2 on 2020-11-17 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_name', models.CharField(max_length=64)),
                ('initial_price', models.IntegerField()),
            ],
        ),
    ]
