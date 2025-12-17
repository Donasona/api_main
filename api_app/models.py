from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Productmodel(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    product_name = models.CharField(max_length=100)

    product_price = models.IntegerField()

    product_color = models.CharField(max_length=50)