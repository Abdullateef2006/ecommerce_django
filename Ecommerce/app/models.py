from django.db import models
import uuid
from django.contrib.auth.models import User

class Category(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4)
    title =  models.CharField(max_length=50)
    


    def __str__(self):
        return self.title
    
    
class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=250)
    description =  models.TextField()
    priceOne = models.IntegerField(default=0)
    priceTwo = models.IntegerField(default=0)
    image = models.FileField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uu_id = models.UUIDField(default=uuid.uuid4)
    quantity = models.IntegerField(default=1)
    item_remaining = models.IntegerField(default=1)
    sizes = models.ManyToManyField(Size, blank=True, default="meduim")
    colors = models.ManyToManyField(Color, blank=True, default="black")

    
    
    


    def __str__(self):
        return self.title
    
class Cart(models.Model):
    '''Model definition for cart.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    is_added = models.BooleanField(default=False)
    name = models.ForeignKey(Products, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(default=0)
    size = models.ForeignKey(Size, default="meduim", on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color,  default="red", on_delete=models.SET_NULL, null=True)
    
    
    
    def price(self):
        return self.name.priceTwo * self.quantity

    class Meta:

        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return f"{self.name.title} - {self.name.priceTwo * self.quantity}" 
    
    
class Wishlist(models.Model):
    '''Model definition for Wishlist.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    is_added = models.BooleanField(default=False)
    name = models.ForeignKey(Products, on_delete=models.CASCADE, default='')

    class Meta:
        '''Meta definition for Wishlist.'''

        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.name.title



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=100, blank=True)
    home_address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    '''Model definition for Profile.'''

    class Meta:
        '''Meta definition for Profile.'''

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username
    
    # models.py
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.reference} - {self.user.username}'

    