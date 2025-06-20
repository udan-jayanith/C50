from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"\n username: {self.username} \n"
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')

class URL(models.Model):
    title = models.CharField(max_length=1024)
    url = models.CharField(max_length=1083)
    timestamp = models.DateTimeField(default=datetime.now)

    def serialize(self):
        return {
            'title': self.title,
            'url': self.url,
            'timestamp': self.timestamp.ctime(),
            'pk': self.pk
        }


#order_by("-timestamp").all()
class Library(models.Model):
    libraryName = models.CharField(max_length=124)
    libraryDescription = models.TextField()
    urlList = models.ManyToManyField(URL, symmetrical=False, blank=True)
    visibility = models.CharField(max_length=124)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_libraries')

    def addURL(self, title, url):
        urlModel = URL(title = title, url = url)
        urlModel.save()
        self.urlList.add(urlModel)

    def visibilityToPublic(self):
        self.visibility = 'public'
    
    def visibilityToPrivate(self):
        self.visibility = 'private'

    def getCurrentVisibility(self):
        return self.visibility
    
    def getLibrary(self):
        return {
            'libraryName': self.libraryName,
            'libraryDescription': self.libraryDescription,
            'visibility': self.getCurrentVisibility(),
            'libraryPk': self.pk,
            'ownerUsername': self.owner.user.username,
            'ownerPk': self.owner.user.pk
        }
    
    def getURL_List(self, pageNo):
        i = (pageNo-1)*10
        j = min(self.urlList.count(), i+10)
        if j <= i:
            return []
        
        urlList = self.urlList.order_by("-timestamp").all()[i:j]
        return [url.serialize() for url in urlList]


