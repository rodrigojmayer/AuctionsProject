from django.urls import path

from . import views

"""agregado para las imagenes:
from django.conf import settings
from django.conf.urls.static import static"""
from django.conf import settings
from django.conf.urls.static import static

"""agregado para los gets:"""
app_name="auctions_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("create_category/", views.create_category, name="create_category"),
    path("listing_page/<str:auction>", views.listing_page, name="listing_page"),
    path("create_bid/", views.create_bid, name="create_bid"),
    path("create_comment/", views.create_comment, name="create_comment"),
    path("create_answer/<str:id_comment>", views.create_answer, name="create_answer"),
    path("watch_list/", views.watch_list, name="watch_list"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:id_category>", views.category, name="category"),
    path("check_auction/", views.check_auction, name="check_auction"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#agregado para las imagenes: + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


