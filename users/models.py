from django.db import models

class CategoryMaster(models.Model):
    category_name=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    modified_by=models.IntegerField(blank=True,null=True)
    created_by=models.IntegerField(blank=True,null=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table="CategoryMaster"
        ordering = ["created_at"]
 
class SubCategory(models.Model):
    categroy=models.ForeignKey(CategoryMaster,on_delete=models.CASCADE,related_name='category_details')
    product_name=models.IntegerField(blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    quantity=models.IntegerField(blank=True,null=True)
    modified_at=models.DateTimeField(auto_now=True)
    modified_by=models.IntegerField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table="SubCategory"
        ordering = ["created_at"]
   