# Generated by Django 3.1.2 on 2020-11-23 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20201119_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='id_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='id_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='auction_active',
            field=models.IntegerField(default=1),
        ),
    ]
