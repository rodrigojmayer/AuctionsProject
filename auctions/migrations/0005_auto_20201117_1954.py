# Generated by Django 3.1.2 on 2020-11-17 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='image',
            field=models.BinaryField(blank=True),
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='auction_category',
            field=models.ManyToManyField(blank=True, related_name='categories', to='auctions.Category'),
        ),
    ]
