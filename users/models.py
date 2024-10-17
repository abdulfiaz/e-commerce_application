from django.db import models
from adminapp.models import *

class CategoryMaster(models.Model):
    category_name=models.CharField(max_length=200,null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    modified_by=models.IntegerField(blank=True,null=True)
    created_by=models.IntegerField(blank=True,null=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table="category_master"
        ordering = ["created_at"]
 
class SubCategory(models.Model):
    categroy=models.ForeignKey(CategoryMaster,on_delete=models.CASCADE)
    product_name=models.CharField(blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    quantity=models.IntegerField(blank=True,null=True)
    modified_at=models.DateTimeField(auto_now=True)
    modified_by=models.IntegerField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table="sub_category"
        ordering = ["created_at"]
   


class Cart(models.Model):
    product=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='cart')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    class Meta:
        db_table="addcart"
