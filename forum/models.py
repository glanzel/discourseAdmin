from django.db import models

# Create your models here.

class Forum(models.Model):
    
    name = models.CharField(max_length=255, null=True, blank=True)

    reads = models.CharField(max_length=255, null=True, blank=True)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
