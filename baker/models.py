from django.conf import settings
from django.db import models
from django.utils import timezone


class Bread(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    description = models.TextField()
    geschnitten = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title + " " +self.text


class Cake(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    fruits = models.TextField()
    geschnitten = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
