from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    content = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="messages",on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]
    
    def __str__(self):
        return self.content
        
    def last_10_message():
        return Message.objects.all()[:10][::-1]