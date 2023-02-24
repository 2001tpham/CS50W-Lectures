from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create-listing', views.create_lising, name='create-listing'),
    path('filter', views.filter, name='filter'),
    path('listing/<int:listingid>', views.listing, name='listing'),
    path('addListing/<int:listingid>', views.addListing, name='add_watchlist_item'),
    path('removeListing/<int:listingid>', views.removeListing, name='remove_watchlist_item'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('addComment/<int:listingid>', views.addComment, name='addComment'),
    path('addBid/<int:listingid>', views.addBid, name='add_bid')
]
