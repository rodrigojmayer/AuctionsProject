from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json, math
from django.core import serializers

from django.templatetags.static import static
from jinja2 import Environment

# @csrf_protect
# @csrf_exempt
# @login_required


def environment(**options):
    env = Environment(**options, extensions=['jinja2.ext.loopcontrols'])
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env

from .models import User, AuctionListings, Bids, Comments, Category, WatchLists


@csrf_exempt
@login_required
def index(request):

    print("Siempre entra aca o solo con el indice???????????????????????????")
    all_auctions = AuctionListings.objects.all()
    #all_bids = Bids.objects.all()
    len_auctions = len(all_auctions)
    if len_auctions > 0:
        last_auction = all_auctions[len_auctions-1].id
    else:
        last_auction = 0
    # print(last_auction)
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
            
        print(" ")
        print("The request POST is: ---")
        print(request.POST)
        print("The request FILES is: ---")
        print(request.FILES)
        print("request POST save")
        print(request.POST["_save"])
        print(" ")
        auction_name = request.POST["auction_name"]
        initial_price = request.POST["initial_price"]
        description = request.POST["description"]
        auction_category = request.POST.getlist('auction_category')
        image = request.FILES['image']
        print(" ")
        print(request)
        print(" ")
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
    # print("auction")
    # print(auction)
    auction_data = AuctionListings.objects.get(id=auction)
    actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    actual_comment = Comments.objects.filter(id_auction=auction_data.id)
    comments = Comments.objects.filter(id_auction=auction_data.id)
    err_mess = ""
    if(actual_bid):
        actual_bid = Bids.objects.get(id_auction=auction_data.id)
    # print("user_logged.id")
    # print(user_logged.id)
    print("request POST:")
    print(request.POST)
    # if(request.POST):
    #     print("true")
    # else:
    #     print("false")
    # print("request.method")
    # print(request.method)
    print('request POST ["_place bid"]:')
    if("_place_bid" in request.POST):
        print(request.POST["_place_bid"])
    # if("new_bid" in request.POST):
    #     print("new_bidnew_bid")

        
    
    '''print(auction_data.id)'''
    # if(request.method == "POST"):
            
    #     # if("_place_bid" in request.POST):
    #     if(request.POST["_place_bid"] == "Add to Watchlist"):
    #         already_in_watchlist = WatchLists.objects.filter(id_auction=auction_data,id_user=user_logged)
    #         if(already_in_watchlist):
    #             print("This item is already charged in the watchlist--->")
    #             in_watchlist=already_in_watchlist
    #         else:
    #             print("This item is not already charged in the watchlist--->")
    #             add_watchlist = WatchLists(id_auction=auction_data , id_user=user_logged)
    #             add_watchlist.save()
    #             '''print(add_watchlist)'''
    #             in_watchlist=add_watchlist
    #     else:
    #         '''print(user_logged)
    #         print(auction_data.id)'''
    #         del_watchlist = WatchLists.objects.get(id_auction=auction_data.id,id_user=user_logged.id)
    #         if(del_watchlist):
    #             del_watchlist.delete()
    #         in_watchlist=False
    #         #pass
    #     #elif((request.POST["_place_bid"]))
            
    # else:
    in_watchlist = WatchLists.objects.filter(id_auction=auction_data.id,id_user=user_logged.id)
    if(in_watchlist):
        in_watchlist = "in_watchlist"
    else:
        in_watchlist = "out_watchlist"

    new_bid = request.GET.get('new_bid')
    close_auction = request.GET.get('close_auction')
    new_comment = request.GET.get('new_comment')
    print("new bid:")
    print(new_bid)
    print("close auction:")
    print(close_auction)
    print("new comment:")
    print(new_comment)
    if(new_bid):
        #actual_bid = Bids.objects.filter(id_auction=auction_data.id)
        print("hay una nueva oferta")
        print(actual_bid)
        if(actual_bid):
            print("si ya tenia una oferta anterior")
            #actual_bid = Bids.objects.get(id_auction=auction_data.id)
            if(int(new_bid) > actual_bid.price):
                print("nueva oferta mayor que la anterior")
                actual_bid.delete()
                add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                print("nueva oferta no es mayor que la anterior")
                err_mess = "Your bid is lower than the previous"
        else:
            print("no tenia una oferta anterior")
            if(int(new_bid)>=auction_data.initial_price):
                print("nueva oferta mayor o igual que la inicial")
                add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                print("nueva oferta es menor que la inicial")
                err_mess = "Your bid is lower than the starting price."

    elif(new_bid == "" and new_comment == ""):
        print("no ha ingresado ninguna oferta o comentario")
        err_mess = "You have not entered any bid or comment."
    elif(new_comment):
        add_comment = Comments(id_auction=auction_data, description=new_comment, id_user=user_logged)
        add_comment.save()
    elif(close_auction):
        print("se pidió el cierre de la auction list")
        auction_data.auction_active = 0
        auction_data.save()

    else:
        print("carga inicial de la pagina")
        
            
            
            
    return render(request, "auctions/listing_page.html", {
        "auction_data": auction_data,
        "in_watchlist": in_watchlist,
        "user_logged" : user_logged,
        "actual_bid" : actual_bid,
        "err" : err_mess,
        "comments" : comments,
    })

def create_bid(request):
    print("---entra al create_bid---")

    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    if(actual_bid):
        actual_bid = Bids.objects.get(id_auction=auction_data.id)
    bid_added = request.GET['new_bid']
    user_logged = request.user
    err_mess = ""
    #print("create bid prints:")
    #print(bid_added)
    if(bid_added):
        #actual_bid = Bids.objects.filter(id_auction=auction_data.id)
        print("hay una nueva oferta")
        print(actual_bid)
        if(actual_bid):
            print("si ya tenia una oferta anterior")
            #actual_bid = Bids.objects.get(id_auction=auction_data.id)
            if(int(bid_added) > actual_bid.price):
                print("nueva oferta mayor que la anterior")
                actual_bid.delete()
                add_bid = Bids(id_auction=auction_data, price=int(bid_added), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                print("nueva oferta no es mayor que la anterior")
                err_mess = "Your bid is lower than the previous"
        else:
            print("no tenia una oferta anterior")
            if(int(bid_added)>=auction_data.initial_price):
                print("nueva oferta mayor o igual que la inicial")
                add_bid = Bids(id_auction=auction_data, price=int(bid_added), id_user=user_logged)
                add_bid.save()
                actual_bid = add_bid
            else:
                print("nueva oferta es menor que la inicial")
                err_mess = "Your bid is lower than the starting price."

    else:
        print("no ha ingresado ninguna oferta o comentario")
        err_mess = "You have not entered any bid."

    
    
    return render(request, "auctions/create_bid.html", {
        "auction_data": auction_data,
        "bid_added": bid_added,
        "err" : err_mess
        
    })

def create_comment(request):
    print("el request method es este----->")
    print(request.method)
    #auction_data_bid = AuctionListings.objects.get(id=request.GET['auction_get'])
    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    user_logged = request.user
    comment_added = request.GET['new_comment']
    
    
    err_mess = ""

    print("create comment print:")
    print(comment_added)
    if(comment_added == ""):
        print("no ha ingresado ningun comentario")
        err_mess = "You have not entered any comment."
    else:
        print(" ha ingresado comentario")
        comment_duplicated = Comments.objects.filter(id_auction=auction_data, description=comment_added, id_user=user_logged.id)
        if comment_duplicated:
            print("comment duplicated --- ")
            print(comment_duplicated)
            err_mess = "Duplicate question."
        else:
            print("comment not duplicated----")
            add_comment = Comments(id_auction=auction_data, description=comment_added, id_user=user_logged)
            add_comment.save()
   
    
    
    return render(request, "auctions/create_comment.html", {
        "auction_data": auction_data,
        "comment_added": comment_added,
        "err" : err_mess

    })

def create_answer(request, id_comment):
    auction_data = AuctionListings.objects.get(id=request.GET['auction_data'])
    print("this is the comment to add an answer:")
    print(id_comment)

    answer_added = request.GET['new_answer']
    
    
    err_mess = ""

    # print("create anser print:")
    # print(answer_added)
    if(answer_added == ""):
        print("no ha ingresado ninguna respuesta")
        err_mess = "You have not entered any answer."
    else:
        print(" ha ingresado comentario")
        # add_answer = Comments(id_auction=auction_data, answer=answer_added, id_user=user_logged)
        # add_answer.save()
        add_answer = Comments.objects.get(id=id_comment)
        add_answer.answer = answer_added
        add_answer.save()
   
    
    
    return render(request, "auctions/create_answer.html", {
        "auction_data": auction_data,
        "answer_added": answer_added,
        "err" : err_mess

    })

def watch_list(request):
    print("--- Entering to the watch_list view ---")
    all_auctions = AuctionListings.objects.all()
    all_bids = Bids.objects.all()
    user_logged = request.user
    my_watch_list = WatchLists.objects.filter(id_user=user_logged)
    # len_auctions = len(my_watch_list)
    # print("--- len_auctions ---")
    # print(len_auctions)
    # if(len_auctions != 0):
        # last_auction = my_watch_list[len_auctions-1]
        # last_auction_id = last_auction.id_auction.id
    # else:
        # last_auction_id = 0
    # print("the last auction is: ")
    # print( last_auction.id_auction.id)
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
        # "last_auction_id" : last_auction_id,
    })

# @csrf_protect
@csrf_exempt
@login_required
def categories(request):
    # print("Entrando al categoriesssssssDDDDDDDDDDDDDDDDDDDDDDDD")
    all_categories = Category.objects.all().order_by('category_name')
    if request.method == "POST":
        # print(all_categories[0])

        response = {}
        response = serializers.serialize("json",all_categories)

        # print("this is the json")
        # print(response)
        # categories_array = []   
        # for each_category in all_categories:
        #     # print(each_category)
        #     each_category=str(each_category)
        #     categories_array.append(each_category) 
        
        return JsonResponse({
            # "categories_array":categories_array,
            "categories_array":response,
            "message": "Profile followed successfully."
        }
        , status=201)
    if request.method == "GET":
        # # data = json.loads(all_categories)
        return render(request, "auctions/categories.html", {
            "all_categories" : all_categories,
        }) 

def category(request, id_category):

    category = Category.objects.get(id=id_category)
    auction_listing_category = AuctionListings.objects.filter(auction_category__id=id_category)
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
        # response = {}
        # response = serializers.serialize("json", "holis")
        # var = {request.}
        # data = json.loads(request)
        new_auction_name=request.POST.get('name')
        auction_data = AuctionListings.objects.filter(name=new_auction_name, auction_active=1)
        if(auction_data):
            print("There is already an active auction with that name")
            auction_repeated = True
        else:
            print("There is no active auction with that name")
            auction_repeated = False
        # print(" el nname esssssssssssssssssss")
        # print(name)
        # print (request.body['Content-Type'])
        # response = serializers.serialize("json", Category.objects.all())
        # response={request.description}

        return JsonResponse({
            "auction_repeated":auction_repeated,
        }
        , status=201)


        
def add_in_watch_list(request, auction):
    user_logged = request.user
    # print("auction")
    # print(auction)
    auction_data = AuctionListings.objects.get(id=auction)
    actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    actual_comment = Comments.objects.filter(id_auction=auction_data.id)
    comments = Comments.objects.filter(id_auction=auction_data.id)
    err_mess = ""
    if(actual_bid):
        actual_bid = Bids.objects.get(id_auction=auction_data.id)
    # print("user_logged.id")
    # print(user_logged.id)
    print("request POST:")
    # print(request.POST)
    # if(request.POST):
    #     print("true")
    # else:
    #     print("false")
    # print("request.method")
    # print(request.method)
    print('request POST ["_place bid"]:')
    # if("_place_bid" in request.POST):
        # print(request.POST["_place_bid"])
    # if("new_bid" in request.POST):
    #     print("new_bidnew_bid")

        
    
    '''print(auction_data.id)'''
    if(request.method == "GET"):
            
        # if("_place_bid" in request.POST):
        if(request.GET["_place_bid"] == "Add to Watchlist"):
            already_in_watchlist = WatchLists.objects.filter(id_auction=auction_data,id_user=user_logged)
            if(already_in_watchlist):
                print("This item is already charged in the watchlist--->")
                in_watchlist=already_in_watchlist
            else:
                print("This item is not already charged in the watchlist--->")
                add_watchlist = WatchLists(id_auction=auction_data , id_user=user_logged)
                add_watchlist.save()
                '''print(add_watchlist)'''
                in_watchlist=add_watchlist
        else:
            '''print(user_logged)
            print(auction_data.id)'''
            del_watchlist = WatchLists.objects.get(id_auction=auction_data.id,id_user=user_logged.id)
            if(del_watchlist):
                del_watchlist.delete()
            in_watchlist=False
            #pass
        #elif((request.POST["_place_bid"]))
            
    # else:
    #     in_watchlist = WatchLists.objects.filter(id_auction=auction_data.id,id_user=user_logged.id)
    #     new_bid = request.GET.get('new_bid')
    #     close_auction = request.GET.get('close_auction')
    #     new_comment = request.GET.get('new_comment')
    #     print("new bid:")
    #     print(new_bid)
    #     print("close auction:")
    #     print(close_auction)
    #     print("new comment:")
    #     print(new_comment)
    #     if(new_bid):
    #         #actual_bid = Bids.objects.filter(id_auction=auction_data.id)
    #         print("hay una nueva oferta")
    #         print(actual_bid)
    #         if(actual_bid):
    #             print("si ya tenia una oferta anterior")
    #             #actual_bid = Bids.objects.get(id_auction=auction_data.id)
    #             if(int(new_bid) > actual_bid.price):
    #                 print("nueva oferta mayor que la anterior")
    #                 actual_bid.delete()
    #                 add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
    #                 add_bid.save()
    #                 actual_bid = add_bid
    #             else:
    #                 print("nueva oferta no es mayor que la anterior")
    #                 err_mess = "Your bid is lower than the previous"
    #         else:
    #             print("no tenia una oferta anterior")
    #             if(int(new_bid)>=auction_data.initial_price):
    #                 print("nueva oferta mayor o igual que la inicial")
    #                 add_bid = Bids(id_auction=auction_data, price=int(new_bid), id_user=user_logged)
    #                 add_bid.save()
    #                 actual_bid = add_bid
    #             else:
    #                 print("nueva oferta es menor que la inicial")
    #                 err_mess = "Your bid is lower than the starting price."

    #     elif(new_bid == "" and new_comment == ""):
    #         print("no ha ingresado ninguna oferta o comentario")
    #         err_mess = "You have not entered any bid or comment."
    #     elif(new_comment):
    #         add_comment = Comments(id_auction=auction_data, description=new_comment, id_user=user_logged)
    #         add_comment.save()
    #     elif(close_auction):
    #         print("se pidió el cierre de la auction list")
    #         auction_data.auction_active = 0
    #         auction_data.save()

    #     else:
    #         print("carga inicial de la pagina")
            
            
            
            
    return render(request, "auctions/listing_page.html", {
        "auction_data": auction_data,
        "in_watchlist": in_watchlist,
        "user_logged" : user_logged,
        "actual_bid" : actual_bid,
        "err" : err_mess,
        "comments" : comments,
    })