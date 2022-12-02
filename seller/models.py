from django.db import models

# Create your models here.
class Seller(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True)
    address = models.TextField(max_length = 200, null=True, blank= True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length= 50)
    pic = models.FileField(upload_to= 'seller_profile', default= 'sad.jpg')
    dob = models.DateField(null= True, blank= True)
    gender = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.first_name


class Product(models.Model):
    name = models.CharField(max_length= 30)
    des = models.CharField(max_length=330)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    pic = models.FileField(upload_to= 'products', default='woman.jpg')
    
    def __str__(self) -> str:
        return self.name

