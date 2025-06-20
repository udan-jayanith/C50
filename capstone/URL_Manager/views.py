import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from .models import *

import requests
from bs4 import BeautifulSoup

#libraries used in this project beautifulsoup4 , requests

# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile(user = user)
            profile.save()
        except IntegrityError:
            return render(request, "authentication/signin.html", {
                'message': "User name already taken."
            })
        
        login(request, user)
        return redirect('index')
    else:
        return render(request, "authentication/signin.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "authentication/login.html", {
                'message': "Invalid username and/or password."
            })
    else:
        return render(request, "authentication/login.html")

def logout_view(request):
    logout(request)
    return redirect('index')

def libraries(req, ownerPk):
    profile = Profile.objects.filter(user = User.objects.filter(pk = ownerPk).get()).get()
    if req.method == "GET":
        return render(req, 'libraries/libraries.html', {
            'profile': profile
        })
    elif req.method == "POST":
        if req.user.pk != ownerPk:
            return JsonResponse({
                'error': "Invalid request."
            })
        
        libraryName = req.POST['library-name']
        if libraryName.strip() == "":
            return JsonResponse({
                'error': 'Library name must not be empty.'
            })
        libraryDescription = req.POST['library-description']
        
        visibilityMod = req.POST['visibility-mod'].strip()
        if visibilityMod == 'private' or visibilityMod == 'public':
            libraryModel = Library(libraryName = libraryName, libraryDescription = libraryDescription, owner = profile, visibility = visibilityMod)
            libraryModel.save()
            return JsonResponse({
                'redirect': reverse('library', kwargs={
                    'libraryPk': libraryModel.pk
                })
            })
    
def getLibraries(req, ownerPk, pageNo):
    owner = Profile.objects.filter(user = User.objects.filter(pk = ownerPk).get()).get()
    libraryList = None

    if not req.user.is_authenticated or req.user.pk != ownerPk:
        libraryList = owner.my_libraries.filter(owner = owner, visibility = 'public')
    else:
        libraryList = owner.my_libraries.all()

    i = (pageNo-1)*10
    j = min(libraryList.count(), i+10)
    if j <= i:
        return JsonResponse({
            'list': []
        }) 
    
    return JsonResponse({
        "list": [lib.getLibrary() for lib in libraryList[i:j]]
    })

def publicLibraries(req):
    return render(req ,'libraries/publicLibraries.html')

def getPublicLibraries(req, pageNo):
    libraryList = Library.objects.filter(visibility='public').all()

    i = (pageNo-1)*10
    j = min(libraryList.count(), i+10)
    if j <= i:
        return JsonResponse({
            'list': []
        }) 
    
    return JsonResponse({
        "list": [lib.getLibrary() for lib in libraryList[i:j]]
    })

def myLibrariesPage(req):
    return redirect('libraries', ownerPk = req.user.pk)

def library(req, libraryPk):
    library = Library.objects.filter(pk = libraryPk).get()
    if library.owner.pk != req.user.pk and library.getCurrentVisibility() == 'private':
        return JsonResponse({
            'error': 'You are not authorized to view this library.'
        })
    
    if req.method == "GET":
        return render(req, 'libraries/library.html', {
            'library': library.getLibrary()
        })
    
    if req.user.pk != library.owner.pk:
            return JsonResponse({"error": "Access denied."})
    
    if req.method == "POST":
        url = req.POST['url']
        if url.strip() == "":
            return JsonResponse({"error": "URL required."})

        title = req.POST['title']
        if title.strip() == "":
            title = getTitle(url)
        
        if title.strip() == "":
            return JsonResponse({'error': "Title couldn't be detected. You may have to type in the title manually."})

        urlModel = URL(url = url, title=title)
        urlModel.save()
        library.urlList.add(urlModel)
        return JsonResponse({'title': title})
    elif req.method == "PUT":
        data = json.loads(req.body)
        url = data.get('url')
        if url.strip() == "":
            return JsonResponse({"error": "URL required."})

        title = data.get('title')
        if title.strip() == "":
            title = getTitle(url)
        
        if title.strip() == "":
            return JsonResponse({'error': "Title couldn't be detected. You may have to type in the title manually."})
        
        urlItemPk = int(data.get('url-item-pk'))
        if urlItemPk == 0:
            return JsonResponse({'error': 'url-item-pk may be invalid.'})
        
        urlModel = URL.objects.filter(pk = urlItemPk).get()
        urlModel.url = url
        urlModel.title = title
        urlModel.save()
        return JsonResponse({
            'title': title,
            'url': url
        })
    elif req.method == "DELETE":
        urlItemPk = int(json.loads(req.body).get('url-item-pk'))
        if urlItemPk == 0:
            return JsonResponse({'error': 'url-item-pk may be invalid.'})
        
        urlModel = URL.objects.filter(pk = urlItemPk).get()
        urlModel.delete()
        return JsonResponse({})

def getUrls(req, libraryPk, pageNo):
    library = Library.objects.filter(pk = libraryPk).get()
    if library.owner.pk != req.user.pk and library.getCurrentVisibility() == 'private':
        return JsonResponse({
            'error': 'You are not authorized to view this library.'
        })

    return JsonResponse({
        'list': library.getURL_List(pageNo)
    })

def deleteLibrary(req, libraryPk):
    library = Library.objects.filter(pk = libraryPk).get()
    if library.owner.pk != req.user.pk:
        return JsonResponse({
            'error': 'You are not authorized to delete this library.'
        })

    library.delete()
    return JsonResponse({
        'redirect': reverse('myLibraries')
    })

def editLibrary(req, libraryPk):
    library = Library.objects.filter(pk = libraryPk).get()
    if library.owner.pk != req.user.pk:
        return JsonResponse({
            'error': 'You are not authorized to edit this library.'
        })
    
    libraryName = req.POST['library-name']
    if libraryName.strip() == "":
            return JsonResponse({
                'error': 'Library name must not be empty.'
            })
    libraryDescription = req.POST['library-description']
        
    visibilityMod = req.POST['visibility-mod'].strip()
    if not (visibilityMod == 'private' or visibilityMod == 'public'):
        return JsonResponse({
            'error': "Invalid visibility mod."
        })
    
    library.libraryName = libraryName
    library.libraryDescription = libraryDescription
    library.visibility = visibilityMod
    library.save()
    return JsonResponse({})
        
def index(req):
    if not req.user.is_authenticated :
        return redirect('publicLibraries')
    else:
        profile = Profile.objects.filter(user = req.user).get()

        try:
            myUrls = profile.my_libraries.all().filter(libraryName = 'My Urls').get()
        except:
            myUrls = Library(owner=profile, libraryName='My Urls', libraryDescription="")
            myUrls.visibilityToPrivate()
            myUrls.save()
        
        return redirect('library', libraryPk = myUrls.pk)
        
"""Returns the title of the given website url."""
def getTitle(websiteURL):
    title = ""
    req = requests.get(websiteURL, timeout=5)
    if 'text/html' not in req.headers.get('Content-Type', '') or req.status_code != 200:
        return title

    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.title.string

    return title