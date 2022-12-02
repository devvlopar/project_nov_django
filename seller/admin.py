from django.contrib import admin
from .models import Seller , Product

# Register your models here.
admin.site.register(Seller)

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display= ['name', 'des', 'price', 'quantity']