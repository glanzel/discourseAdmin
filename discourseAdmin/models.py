import uuid
from django.db import models
from django.contrib.auth.models import User
from cProfile import label

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
    
    name = models.CharField(max_length=255, null=True)

    description = models.CharField(max_length=255, null=True, blank=True)
    
    discourse_group_id = models.IntegerField(null=True, unique=True)
    
    is_department = models.BooleanField(null=True, default=0, blank=True)

    update_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

    members = models.ManyToManyField(User, through='User_Groups')
    
    def __str__(self):
        if self.name !=None: return self.name
        else: return "leer"
    
    class Meta:
        ordering = ['-id']


class Participant(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(dGroup, on_delete=models.CASCADE, null=True, blank=True, related_name="department")
    discourse_user = models.CharField(max_length=255, null=True, blank=True)
    #groups = models.ManyToManyField(Group, through='User_Groups', related_name="groups")

    def __str__(self):
        return "test2" #self.discourse_user+" "

from django.contrib.auth.models import User

class User_Groups(models.Model):
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    group = models.ForeignKey(dGroup, null=True, blank=True, on_delete=models.CASCADE)

    rights = models.BooleanField(null=True, default=0, blank=True)

    update_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

    def isGroupAdmin(user_id, group_id):
        try: is_admin = User_Groups.objects.get(user_id=user_id, group_id = group_id)
        except: None
        else: 
            if (is_admin.rights != None) and (is_admin.rights > 0) : return True 
        return False 

    class Meta:
        ordering = ['-id']
        unique_together = ('user', 'group',)
 