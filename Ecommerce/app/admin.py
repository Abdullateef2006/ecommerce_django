from django.contrib import admin

from .models import *




admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Transaction)

admin.site.register(Wishlist)



# Register your models here.
