from enum import unique
from unicodedata import decimal
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.




class Block_category(models.Model): #category Gomi , sozai, Syouhinn
    name = models.CharField("block_type", max_length=100)
    def __str__(self):
        return self.name

class object_type(models.Model): #Sub catergoy for each category
    name = models.CharField("object_type", max_length=100)
    def __str__(self):
        return self.name

class people(models.Model):
    name =  models.CharField("name", max_length=100)
    def __str__(self):
        return self.name

class amount_units(models.Model): #kg, g, 
    name =  models.CharField("amount_units", max_length=100)
    def __str__(self):
        return self.name

def upload_image_path(instance,filename):
    ext=filename.split(".")[-1]
    return '/'.join(['image', str(instance.blockid.id)+"_"+str(instance.date)+str(".")+str(ext)])


class Block(models.Model):
    name= models.CharField(max_length=100)
    unique_id = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) #Block creation
    date = models.DateTimeField(default=timezone.now) #date of block real creation i.e collection date
    img = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    #Link to other data 
    amount_type = models.ForeignKey(amount_units,verbose_name="amount_units",on_delete=models.PROTECT)
    creater = models.ForeignKey(people,verbose_name="name",on_delete=models.PROTECT)
    block_type=models.ForeignKey(Block_category,verbose_name="block_type",on_delete=models.PROTECT)
    object_type=models.ForeignKey(object_type,verbose_name="object_type",on_delete=models.PROTECT)
