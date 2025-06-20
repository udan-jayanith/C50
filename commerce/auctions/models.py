from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    def __str__(self):
        return f"\n username: {self.username} \n"
    pass

class Listing(models.Model):
    itemName = models.CharField(max_length=360)
    itemImgURL = models.CharField(max_length=2083)
    itemDescription = models.TextField()
    currentBid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myListings')
    createdDate = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=124)

    def __str__(self):
        return f'\n item-name: {self.itemName}, currentBid: {self.currentBid}, owner: {self.owner.username} \n'
    
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidAmount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myBids")

    def __str__(self):
        return f'\n item: {self.listing.itemName}, bidAmount: {self.bidAmount}, bidder: {self.bidder.username} \n'
    
class Inbox(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inbox") 

class Comments(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myComments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'\n comment: {self.comment}, commenter: {self.commenter.username}, item: {self.listing.itemName} \n'

class WatchList(models.Model):
    auctionItem = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchList")


