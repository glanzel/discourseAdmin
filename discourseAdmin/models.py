from django.db import models

# Create your models here.

# class User(models.Model):
#     
#     username = models.CharField(max_length=255, null=True, blank=True)
# 
#     password = models.CharField(max_length=255, null=True, blank=True)
# 
#     email = models.CharField(max_length=255, null=True, blank=True)
# 
#     update_date = models.DateTimeField(auto_now=True)
#     create_date = models.DateTimeField(auto_now_add=True)
# 
#     class Meta:
#         ordering = ['-id']

from django.contrib.auth.models import User

class Group(models.Model):
    
    name = models.CharField(max_length=255, null=True, blank=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(User, through='User_Groups')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']

class User_Groups(models.Model):
    
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    group_id = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    rights = models.IntegerField(null=True, default=None)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
