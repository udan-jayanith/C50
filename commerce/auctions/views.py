from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from datetime import datetime

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def addListing(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    if req.method == "POST":
        itemName = req.POST['item-name']
        itemImgURL = req.POST['item-img-url']
        itemDescription = req.POST['item-description']
        currentBid = req.POST['starting-bid']
        category = req.POST['category'].lower()
        owner = req.user

        listing = Listing(owner=owner, itemName=itemName, itemImgURL=itemImgURL, itemDescription=itemDescription, currentBid=currentBid, createdDate=datetime.now(), category=category)
        listing.save()
        return redirect('auctions:listing', pk = listing.pk)
    else:
        return render(req, 'auctions/addListing/index.html', {
            'user': req.user
        })

def isInWatchlist(auctionItem, user):
    return auctionItem.watchlist.all().filter(user = user).first() != None

def listingPage(req, pk):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    auctionItem = Listing.objects.filter(pk = pk).get()
    return render(req, 'auctions/listingPage/index.html', {
        "item": auctionItem,
        'isOwner': True if auctionItem.owner.username == req.user.username else False,
        'comments': auctionItem.comments.all(),
        'isInWatchlist': isInWatchlist(auctionItem, req.user)
    })

def categoryPage(req):
    res = set()
    listings = Listing.objects.all()
    for item in listings:
        res.add(item.category)

    return render(req, 'auctions/category/index.html', {
        'res': res
    })

def addComment(req):
    if req.method != "POST":
        return HttpResponse('invalid method.')
    elif not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    pk = req.POST["pk"]
    listing = Listing.objects.all().filter(pk=pk).get()
    comment = Comments(comment=req.POST["comment"], commenter=req.user, listing=listing)
    comment.save()
    return HttpResponse('ok')

def sendMessageToInbox(user, msg):
    inbox = Inbox(message = msg, user = user)
    inbox.save()

def placeBid(req, pk):
    if req.method != "POST":
        return HttpResponse('invalid method.')
    elif not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    bidAmount = req.POST['bid-amount']
    listing = Listing.objects.all().filter(pk=pk).get()
    if listing.currentBid >= int(bidAmount):
        sendMessageToInbox(req.user ,f'Bid for {listing.itemName} cannot be placed. Your bid must exceed the current bid on that item..')
        return HttpResponse('This bid cannot be placed.')
    listing.currentBid = int(bidAmount)
    listing.save()
    bid = Bid(listing=listing, bidAmount = int(bidAmount), bidder = req.user)
    bid.save()
    return HttpResponse('ok')

def watchlist(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    if req.method == "POST":
        pk = req.POST["pk"]
        listing = Listing.objects.all().filter(pk=pk).get()
        if isInWatchlist(listing, req.user):
            saves = listing.watchlist.all().filter(user = req.user).all()
            for save in saves:
                save.delete()
        else:
            watchList = WatchList(auctionItem=listing, user=req.user)
            watchList.save()

        return HttpResponse('ok')
    else:
        watchlist = WatchList.objects.all().filter(user=req.user)
        return render(req, "auctions/watchlist/index.html", {
            'watchlist': watchlist
        })
    
def categoryFilter(req, category):
    listings = Listing.objects.all().filter(category = category)
    return render(req, 'auctions/category/filter/index.html', {
        'category': category.capitalize(),
        'listings': listings.all()
    })
    
def endAuction(req, pk):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    auctionItem = Listing.objects.all().filter(pk = pk).get()
    if req.user != auctionItem.owner:
        return HttpResponse(f"You don't have permission to end the auction.")
    
    bidders = auctionItem.bids.all()
    max = bidders.first()
    losers = set()
    for bidder in bidders:
        if max.bidAmount < bidder.bidAmount:
            max = bidder
            losers.add(max.bidder)
        elif bidder != bidders.first():
            losers.add(bidder.bidder)

    itemName = auctionItem.itemName
    for loser in losers:
        sendMessageToInbox(loser, f'You lose the bid for {itemName}.')

    winnerName = 'No one'
    if max != None:
        sendMessageToInbox(max.bidder, f"You won the bid for {itemName}.") 
        winnerName = max.bidder.username
    
    auctionItem.delete()
    return HttpResponse(f'{winnerName} won the bid for {itemName}')
    
def inbox(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect(reverse("auctions:login"))
    
    myInbox = req.user.inbox.all()
    return render(req, 'auctions/inbox/index.html', {
        'myInbox': myInbox
    })