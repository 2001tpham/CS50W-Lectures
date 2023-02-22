from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category, Listing

from .models import User


def index(request):
    return render(request, "auctions/index.html")


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

        created_listing = Listing(
            price = price,
            name = name,
            description = description,
            image = image,
            is_active = True,
            listing_category = category,
            user = user
        )

        created_listing.save()

        return HttpResponseRedirect(reverse('index'))

