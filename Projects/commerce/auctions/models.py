from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.category}'

class Listing(models.Model):
    price = models.FloatField(max_length=100)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listing_category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_owner')

    def __str__(self):
        return f'{self.name}'

