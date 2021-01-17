from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    done = models.BooleanField()
    owner = models.ForeignKey('auth.User',related_name="notes",on_delete=models.CASCADE)

    class Meta:
        ordering = ['-done']

    def __str__(self):
        return self.title
    
    