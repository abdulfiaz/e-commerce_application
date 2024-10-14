from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class IUMaster(models.Model):
    host_name=models.CharField(max_length=100,blank=True,null=True)
    description=models.CharField(max_length=100,blank=True,null=True)
    host=ArrayField(models.CharField(max_length=200,blank=True,null=True))  
    is_active=models.BooleanField(default=True)
    created_by=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_by=models.IntegerField()
    modified_at=models.DateTimeField(auto_now=True)

    
    class Meta:
        db_table="iu_master"

class CustomUser(AbstractUser):
    
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username=models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_by=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_by=models.IntegerField()
    modified_at=models.DateTimeField(auto_now=True)
    iu_id = models.ForeignKey(IUMaster,on_delete=models.CASCADE)
    temp_otp=models.IntegerField(blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    class Meta:
        db_table="custom_user"
        ordering = ["created_at"]
        unique_together=[('mobile_number','iu_id')]

class RoleMaster(models.Model):
    role_name=models.CharField(max_length=100,blank=True,null=True)
    role_description=models.CharField(max_length=100,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_by=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_by=models.IntegerField()
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="role_master"
        ordering = ["created_at"]

class UserRoleMapping(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    role=models.ForeignKey(RoleMaster,on_delete=models.CASCADE)

    class Meta:
        db_table="user_rolemapping"



