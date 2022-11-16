from django.contrib import admin
from .models import User, AuctionListings, Bids, Comments, Category, WatchLists

from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(WatchLists)