from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json, math
from django.core import serializers
from django.templatetags.static import static
from jinja2 import Environment


def environment(**options):
    env = Environment(**options, extensions=['jinja2.ext.loopcontrols'])
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env

from .models import User, AuctionListings, Bids, Comments, Category, WatchLists


@csrf_exempt
def index(request):
    all_auctions = AuctionListings.objects.all().order_by('-id')
    len_auctions = len(all_auctions)
    if len_auctions > 0:
        last_auction = all_auctions[len_auctions-1].id
    else:
        last_auction = 0
    for auction in all_auctions:
        try:
            all_bids = Bids.objects.get(id_auction=auction.id) 
            auction.initial_price = all_bids.price
        except:
            pass
    
    return render(request, "auctions/index.html", {
        "message": "Aca van los datos de cada auction",
        "all_auctions" : all_auctions,
        "last_auction_id" : last_auction,
        "pepetest": "test de pepito",
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions_app:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions_app:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions_app:index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        auction_name = request.POST["auction_name"]
        initial_price = request.POST["initial_price"]
        description = request.POST["description"]
        auction_category = request.POST.getlist('auction_category')
        image = request.FILES['image']
        user_logged = request.user
        new_listing = AuctionListings(name=auction_name, initial_price=initial_price, description=description, image=image, id_user=user_logged)
        new_listing.save()
        nl = AuctionListings.objects.get(id=new_listing.id)
        for auction_categ in auction_category:
            nl.auction_category.add(auction_categ)
        nl.save()
        if request.POST["_save"] == "Save":
            return HttpResponseRedirect(reverse("auctions_app:index"))
        else:
            all_categories = Category.objects.all().order_by('category_name')
            return render(request, "auctions/create_listing.html", {
                "message": "By post",
                "all_categories": all_categories
            })
        
    else:
        all_categories = Category.objects.all().order_by('category_name')
        return render(request, "auctions/create_listing.html", {
            "message": "By get",
            "all_categories": all_categories
        })


def create_category(request):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        new_category = Category(category_name=category_name)
        new_category.save()
        return render(request, "auctions/create_category.html", {
            "message": "By post"
        })
        
    else:
        all_categories = Category.objects.all()
        return render(request, "auctions/create_category.html", {
            "message": "By get",
            "all_categories": all_categories
        })

def listing_page(request, auction):
    user_logged = request.user
    auction_data = AuctionListings.objects.get(id=auction)
    actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    actual_comment = Comments.objects.filter(id_auction=auction_data.id)
    comments = Comments.objects.filter(id_auction=auction_data.id)
    err_mess = ""
    if(actual_bid):
        actual_bid = Bids.objects.get(id_auction=auction_data.id)
    if("_place_bid" in request.POST):
        print(request.POST["_place_bid"])

    '''print(auction_data.id)'''

    in_watchlist = WatchLists.objects.filter(id_auction=auction_data.id,id_user=user_logged.id)
    if(in_watchlist):
        in_watchlist = "in_watchlist"
    else:
        in_watchlist = "out_watchlist"

    new_bid = request.GET.get('new_bid')
    close_auction = request.GET.get('close_auction')
    new_comment = request.GET.get('new_comment')

    if(new_bid):
        if(actual_bid):
            if(int(new_bid) > actual_bid.price):
                actual_bid.delete()
                add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                err_mess = "Your bid is lower than the previous"

        else:
            if(int(new_bid)>=auction_data.initial_price):
                add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                err_mess = "Your bid is lower than the starting price."

    elif(new_bid == "" and new_comment == ""):
        err_mess = "You have not entered any bid or comment."
    elif(new_comment):
        add_comment = Comments(id_auction=auction_data, description=new_comment, id_user=user_logged)
        add_comment.save()
    elif(close_auction):
        auction_data.auction_active = 0
        auction_data.save()

    else:
        print("initial loading page")
        
    return render(request, "auctions/listing_page.html", {
        "auction_data": auction_data,
        "in_watchlist": in_watchlist,
        "user_logged" : user_logged,
        "actual_bid" : actual_bid,
        "err" : err_mess,
        "comments" : comments,
    })


def create_bid(request):
    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    if(actual_bid):
        actual_bid = Bids.objects.get(id_auction=auction_data.id)
    bid_added = request.GET['new_bid']
    user_logged = request.user
    err_mess = ""
    if(bid_added):
        if(actual_bid):
            if(int(bid_added) > actual_bid.price):
                actual_bid.delete()
                add_bid = Bids(id_auction=auction_data, price=int(bid_added), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                err_mess = "Your bid is lower than the previous"
        else:
            if(int(bid_added)>=auction_data.initial_price):
                add_bid = Bids(id_auction=auction_data, price=int(bid_added), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                err_mess = "Your bid is lower than the starting price."

    else:
        err_mess = "You have not entered any bid."

    return render(request, "auctions/create_bid.html", {
        "auction_data": auction_data,
        "bid_added": bid_added,
        "err" : err_mess
        
    })


def create_comment(request):
    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    user_logged = request.user
    comment_added = request.GET['new_comment']
    err_mess = ""

    if(comment_added == ""):
        err_mess = "You have not entered any question."
    else:
        comment_duplicated = Comments.objects.filter(id_auction=auction_data, description=comment_added, id_user=user_logged.id)
        if comment_duplicated:
            err_mess = "Duplicate question."
        else:
            add_comment = Comments(id_auction=auction_data, description=comment_added, id_user=user_logged)
            add_comment.save()
    
    return render(request, "auctions/create_comment.html", {
        "auction_data": auction_data,
        "comment_added": comment_added,
        "err" : err_mess
    })


def create_answer(request, id_comment):
    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    answer_added = request.GET['new_answer']
    err_mess = ""

    if(answer_added == ""):
        err_mess = "You have not entered any answer."
        return render(request, "auctions/create_answer.html", {
            "auction_data": auction_data,
            "answer_added": answer_added,
            "err" : err_mess
        })

    else:
        add_answer = Comments.objects.get(id=id_comment)
        add_answer.answer = answer_added
        add_answer.save()
        to_question = add_answer.description
    
    return render(request, "auctions/create_answer.html", {
        "auction_data": auction_data,
        "answer_added": answer_added,
        "to_question": to_question,
        "err" : err_mess
    })


def watch_list(request):
    all_auctions = AuctionListings.objects.all()
    all_bids = Bids.objects.all()
    user_logged = request.user
    my_watch_list = WatchLists.objects.filter(id_user=user_logged).order_by('-id')
    for auction in all_auctions:
        try:
            all_bids = Bids.objects.get(id_auction=auction.id) 
            auction.initial_price = all_bids.price
        except:
            pass
       
    for lists in my_watch_list:
        print(lists.id_auction.id)
        print(all_auctions.get(id = lists.id_auction.id))
        
    my_dict = {}
    for lists in my_watch_list:
        my_dict.setdefault(lists.id_auction.id, []).append(all_auctions.get(id = lists.id_auction.id))
    for dicto in my_dict:
        print(my_dict[dicto]) 
    
    return render(request, "auctions/watch_list.html", {
        "message": "Aca van los datos de cada auction",
        "all_auctions" : all_auctions,
        "my_watch_list" : my_watch_list,
        "my_dict" : my_dict,
    })


@csrf_exempt
@login_required
def categories(request):
    all_categories = Category.objects.all().order_by('category_name')

    if request.method == "POST":
        response = {}
        response = serializers.serialize("json",all_categories)
        
        return JsonResponse({
            "categories_array":response,
            "message": "Profile followed successfully."
        }
        , status=201)
    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            "all_categories" : all_categories,
        }) 


def category(request, id_category):
    category = Category.objects.get(id=id_category)
    auction_listing_category = AuctionListings.objects.filter(auction_category__id=id_category).order_by('-id')
    len_auctions = len(auction_listing_category)

    if len_auctions > 0:
        last_auction = auction_listing_category[len_auctions-1].id

    else:
        last_auction = 0

    for auction in auction_listing_category:
        try:
            all_bids = Bids.objects.get(id_auction=auction.id) 
            auction.initial_price = all_bids.price
        except:
            pass

    return render(request, "auctions/category.html", {
        "category" : category,
        "auction_listing_category" : auction_listing_category,
        "last_auction_id" : last_auction,
    })


@csrf_exempt
def check_auction(request):
        new_auction_name=request.POST.get('name')
        auction_data = AuctionListings.objects.filter(name=new_auction_name, auction_active=1)
        if(auction_data):
            auction_repeated = True
        else:
            auction_repeated = False
        return JsonResponse({
            "auction_repeated":auction_repeated,
        }
        , status=201)


@csrf_exempt   
def add_in_watch_list(request, auction):
    auction_data = AuctionListings.objects.get(id=auction)
    user_logged = request.user
    already_in_watchlist = WatchLists.objects.filter(id_auction=auction,id_user=user_logged)
    if(already_in_watchlist):
        already_in_watchlist.delete()
        change_response = "Auction deleted from watchlist"
    else:
        add_watchlist = WatchLists(id_auction=auction_data , id_user=user_logged)
        add_watchlist.save()
        change_response = "Auction added to watchlist"

    return JsonResponse({
        "change_response":change_response,
    }
    , status=201)