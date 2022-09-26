# Generated by Django 3.1.2 on 2020-11-18 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201117_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlistings',
            old_name='auction_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='bids',
            old_name='auction_bid',
            new_name='id_auction',
        ),
        migrations.RenameField(
            model_name='bids',
            old_name='user_bid',
            new_name='id_user',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='auction_comment',
            new_name='id_auction',
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]
