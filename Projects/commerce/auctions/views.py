from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category, Listing, Comment, Bid
from django.db.models import Max

from .models import User


def index(request):
    active_listings = Listing.objects.filter(is_active = True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        'active_listings': active_listings,
        'all_categories': all_categories
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_lising(request):
    all_categories = Category.objects.all()
    if request.method =='GET':
        return render(request, 'auctions/create-listing.html',{
            'all_categories': all_categories
        })
    elif request.method == "POST":
        price = float(request.POST['listing_price'])
        name = request.POST['listing_name']
        description = request.POST['listing_description']
        image = request.POST['listing_image']
        category = Category.objects.get(id=request.POST['listing_category'])

        user = request.user

        bid = Bid(user=user, bid=price)
        bid.save()

        created_listing = Listing(
            price = bid,
            name = name,
            description = description,
            image = image,
            is_active = True,
            listing_category = category,
            user = user
        )

        created_listing.save()

        return HttpResponseRedirect(reverse('index'))

def filter(request):
    if request.method == 'POST':
        filter_selection = request.POST['category']
        category = Category.objects.get(category=filter_selection)
        active_listings = Listing.objects.filter(is_active=True, listing_category=category)
        all_categories = Category.objects.all()
        return render(request, 'auctions/index.html',{
            'active_listings': active_listings,
            'all_categories': all_categories
        })
    
def listing(request, listingid):
    listing = Listing.objects.get(id=listingid)
    is_listing_watchlist = request.user in listing.watchlist.all()
    listing_comments = Comment.objects.filter(listing=listingid)
    

    if listing.price.user == request.user:
        your_bid = True
    else:
        your_bid = False
    return render(request, 'auctions/listing.html',{
        'listing': listing,
        'is_listing_watchlist': is_listing_watchlist,
        'listing_comments': listing_comments,
        'your_bid': your_bid

    })

def addBid(request, listingid):
    bid = float(request.POST['bid_price'])
    bidlisting = Listing.objects.get(id=listingid)
    is_listing_watchlist = request.user in bidlisting.watchlist.all()
    listing_comments = Comment.objects.filter(listing=listingid)

    if bidlisting.price.user == request.user:
        your_bid = True
    else:
        your_bid = False
    if bid > bidlisting.price.bid:
        new_bid = Bid(user=request.user, bid = bid)
        new_bid.save()
        bidlisting.price = new_bid
        bidlisting.save()

        return render(request, 'auctions/listing.html',{
            'listing': bidlisting,
            'is_listing_watchlist': is_listing_watchlist,
            'listing_comments': listing_comments,
            'your_bid': your_bid,
            'bid_message': 'Your bid is in'
        })
    else:
        return render(request, 'auctions/listing.html',{
            'listing': bidlisting,
            'is_listing_watchlist': is_listing_watchlist,
            'listing_comments': listing_comments,
            'your_bid': your_bid,
            'bid_message': 'Your bid is too low'
        })


def addListing(request, listingid):
    listing = Listing.objects.get(id=listingid)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse('listing', args=(listingid,)))

def removeListing(request, listingid):
    listing = Listing.objects.get(id=listingid)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse('listing', args=(listingid,)))

def watchlist(request):
    user = request.user
    watchlist_listings = user.watchlist_item.all()
    return render(request, 'auctions/watchlist.html',{
        'watchlist_listings': watchlist_listings,
    })

def addComment(request, listingid):
    if request.method == 'POST':
        comment = request.POST['comment']
        listing = Listing.objects.get(id=listingid)
        user = request.user

        created_comment = Comment(user=user, listing=listing, comment=comment)
        created_comment.save()
    
    return HttpResponseRedirect(reverse('listing', args=(listingid,)))
