from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.category}'

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bid')
    bid = models.IntegerField()
    def __str__(self):
        return f'{self.user}\'s bid for {self.bid}'
    
class Listing(models.Model):
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='bid_listing')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listing_category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_owner')
    watchlist = models.ManyToManyField(User, related_name='watchlist_item')

    def __str__(self):
        return f'{self.name}'
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment_listing')
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user}\'s comment on {self.listing}'
    


