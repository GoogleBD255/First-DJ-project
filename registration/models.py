from django.db import models
from django.contrib.auth.models import User
from mimetypes import guess_type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile/", blank=True, null=True,default="profile/default.jpg" )


    
    def __str__(self):
        return f"{self.user.username}"
    
