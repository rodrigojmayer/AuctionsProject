from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return f"{self.id}: {self.category_name}"

class AuctionListings(models.Model):
    name = models.CharField(max_length=64)
    initial_price = models.IntegerField()
    auction_category = models.ManyToManyField(Category, blank=True, related_name="categories")
    description = models.CharField(max_length=150, default="")
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    auction_active = models.IntegerField(default=1)
    id_user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name = "user_creator")
    
    """def auction_categories(self):
        return ', '.join([a.category_name for a in self.auction_category.all()])
    #auction_categories.short_description = "category name"
    """
    def __str__(self):
        return f"{self.id}: {self.name} = {self.initial_price}, {self.image} with the categories: {self.auction_category}, created by {self.id_user}"


class Bids(models.Model):
    id_auction = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name = "auction_bids")
    price = models.IntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_bids")

    def __str__(self):
        return f"{self.id}:  bided {self.price} for the auction {self.id_auction} "


class Comments(models.Model):
    id_auction = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, related_name = "auction_comments")
    description = models.CharField(max_length = 150)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_comments")
    answer = models.CharField(null=True, max_length = 150)

    def __str__(self):
        return f"{self.id}: The comment of {self.id_auction} is {self.description}"

class WatchLists(models.Model):
    id_auction = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, related_name = "auction_watch_list")
    id_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_watch_list")

    def __str__(self):
        return f"{self.id}: The watchlist of {self.id_auction} is from the user {self.id_user}"