from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "network/index.html", {
        'pk': request.user.pk if request.user.is_authenticated else ""
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user = user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def addPost(req):
    if not req.user.is_authenticated:
        return redirect('index')

    if req.method != "POST":
        return HttpResponse('Method not allowed.')
    
    post = Post(imgURL=req.POST['img-url'], text=req.POST['text'], user=req.user)
    post.save()
    return HttpResponse('ok')
    
def getPosts(req):
    if req.method != "POST":
        return JsonResponse({"error": "Method not allowed."})

    startingIndex = int(req.POST['s-t'])-1
    if startingIndex < 0:
        return JsonResponse({"error": "s-t must be grater than 0."})

    endIndex = min(Post.objects.count(), startingIndex+10)
    if startingIndex > endIndex:
        return JsonResponse({"error": "end"})

    postList = Post.objects.all().order_by('-created_at')[startingIndex:endIndex]
    return JsonResponse({
        'postLists': [post.serialize(req.user) for post in postList],
        'userPk': req.user.pk
    })

def userpage(req, pk):
    profile = Profile.objects.all().filter(user = User.objects.all().filter(pk = pk).get()).get()
    return render(req, "network/userpage.html", {
        'profile': profile,
        'followingCount': profile.followingCount(),
        'followersCount': profile.followersCount(),
        'isOwner': req.user == profile.user,
        'followed': Profile.objects.all().filter(user = User.objects.all().filter(pk = req.user.pk).get()).get().following.contains(profile) if not req.user.is_anonymous else False,
        'user': req.user 
    })

def getuserPostList(req, pk):
    profile = Profile.objects.all().filter(user = User.objects.all().filter(pk = pk).get()).get()
    
    if req.method != "POST":
        return JsonResponse({"error": "Method not allowed."})

    startingIndex = int(req.POST['s-t'])-1
    if startingIndex < 0:
        return JsonResponse({"error": "s-t must be grater than 0."})

    endIndex = min(profile.user.posts.count(), startingIndex+10)
    if startingIndex > endIndex:
        return JsonResponse({"error": "end"})

    postList = profile.user.posts.all().order_by('-created_at')[startingIndex:endIndex]
    return JsonResponse({
        'postLists': [post.serialize(req.user) for post in postList],
        'userPk':  req.user.pk
    }, safe=False) 

def follow(req):
    if not req.user.is_authenticated:
        return JsonResponse({"error": "Must sign in first."})
    
    profile = Profile.objects.all().filter(user = User.objects.all().filter(pk = req.user.pk).get()).get()
    if req.method == "POST":
        followingPerson = User.objects.all().filter(pk = req.POST['following-pk']).get().profile.get()
        if profile.following.contains(followingPerson):
            profile.following.remove(followingPerson)
            followingPerson.followers.remove(profile)
        else:
            profile.following.add(followingPerson)
            followingPerson.followers.add(profile)
        return JsonResponse({})
    else:
        return render(req, 'network/following.html')
    
def following(req):
    if not req.user.is_authenticated:
        return JsonResponse({"error": "Must sign in first."})

    profile = Profile.objects.all().filter(user = User.objects.all().filter(pk = req.user.pk).get()).get()
    followingPeoples = profile.following.all()
    postList = []
    count = 1
    for person in followingPeoples:
        if count >= 10:
            break
        post = person.user.posts.order_by('-created_at').first()
        if post != None:
            postList.append(post)
        count+=1

    return JsonResponse({
        'postLists': [post.serialize(req.user) for post in postList],
        'userPk':  req.user.pk
    }, safe=False)

def likePost(req, pk):
    if not req.user.is_authenticated:
        return JsonResponse({"error": "Must sign in first."})
    
    post = Post.objects.all().filter(pk = pk).first()
    profile = Profile.objects.all().filter(pk = req.user.pk).first()
    if post.likes.contains(profile):
        post.likes.remove(profile)
    else:
        post.likes.add(profile)
    
    return JsonResponse({})

def deletePost(req, pk):
    if not req.user.is_authenticated:
        return JsonResponse({"error": "Must sign in first."})
    
    post = Post.objects.all().filter(pk = pk).first()
    if post.user != req.user:
        return JsonResponse({"error": "You are unauthorized to delete or edit this post."})
    
    post.delete()
    return JsonResponse({})

def editPost(req, pk):
    if not req.user.is_authenticated:
        return JsonResponse({"error": "Must sign in first."})
    
    post = Post.objects.all().filter(pk = pk).first()
    if post.user != req.user:
        return JsonResponse({"error": "You are unauthorized to delete or edit this post."})
    
    if req.method == "POST":
        imgURL = req.POST['img-url']
        text = req.POST['text']

        post.text = text
        post.imgURL = imgURL
        post.save()
        return JsonResponse({})
    else:
        return JsonResponse(post.serialize(req.user))