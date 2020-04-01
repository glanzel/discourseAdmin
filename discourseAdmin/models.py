from django.db import models
from django.contrib.auth.models import User

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


class dGroup(models.Model):
    
    name = models.CharField(max_length=255, null=True, blank=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(User, through='User_Groups')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(dGroup, on_delete=models.CASCADE, related_name="department")
    discourse_user = models.CharField(max_length=255, null=True, blank=True)
    #groups = models.ManyToManyField(Group, through='User_Groups', related_name="groups")


from django.contrib.auth.models import User

class User_Groups(models.Model):
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    group = models.ForeignKey(dGroup, null=True, blank=True, on_delete=models.CASCADE)

    rights = models.IntegerField(null=True, default=None)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
