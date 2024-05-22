from django.db import models
from django.contrib.auth.models import User
from mimetypes import guess_type
from registration.models import Profile
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    p_img = models.FileField(upload_to="post/",blank=False,null=False)
    date = models.DateTimeField(auto_now_add=True)
    

    def media_type(self):
        type_tuple = guess_type(self.p_img.url, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"
        else:
            raise Exception("Unsupported media type")

    def __str__(self):
        return f"{self.user.username} > {self.title}"

