from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class Meta:
    ordering = ['-created_at']

class User(AbstractUser):
    pass

class Profile(models.Model):
    following= models.ManyToManyField('self', symmetrical=False, related_name='followingList', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followersList', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def followingCount(self):
        return self.following.count()
    
    def followersCount(self):
        return self.followers.count()
  
class Post(models.Model):
    imgURL = models.CharField(max_length=1083)
    text = models.TextField()
    likes = models.ManyToManyField(Profile, related_name='liked', symmetrical=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def likeCount(self):
        return self.likes.count()
    
    def serialize(self, user):
        return {
            "pk": self.pk,
            "imgURL": self.imgURL,
            "text": self.text,
            "likesCount": self.likes.count(),
            "liked": False if not user.is_authenticated else self.likes.contains(Profile.objects.all().filter(pk = user.pk).first()),
            "user": self.user.username,
            "userPk": self.user.pk,  # or user id, whatever you want
            "created_at": self.created_at.ctime(),
            "userPage": reverse('userpage', kwargs={'pk': self.user.pk})
        }

