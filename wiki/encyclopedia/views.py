from django.shortcuts import render, redirect
import random

from django.urls import reverse

from . import util


def index(request):
    title = request.GET.get("q")
    path = ""
    variables = {}
    entry = util.get_entry(title)
    if title != None:
       if entry == None:
           return redirect(f'{reverse('encyclopedia:search-wiki')}?q={title}')
       else:
            return redirect(f'encyclopedia:wiki-content', title=title)
    else:
        path = 'encyclopedia/index.html'
        variables['entries'] = util.list_entries()
        variables['title'] = 'All pages'

    return render(request, path, variables)
    

def wikiContent(req, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(req, "Error.html", {
            "title": title,
            "errorMsg": "Page not found."
        })
    else:
        metadata = util.getEntryMetadata(title)
        return render(req, "encyclopedia/wiki/index.html", {
        "title": title,
        'content':  util.markdownToHTML(entry),
        "createdDate": metadata['created'],
        "lastModifiedDate": metadata['modified']
        })

def search(req):
    q = req.GET.get("q")
    if q == None:
        return render(req, "Error.html", {
            "title": "Invalid query",
            'errorMsg': "Invalid query"
        })

    return render(req, 'encyclopedia/index.html', {
        'entries': util.listContains(q),
        'title': 'Search results'
    })
    
def createNewPage(req):
    if req.method == "POST":
        return addPage(req)
    else :
        return render(req, 'encyclopedia/createNewPage/index.html')

def addPage(req):
    
    if util.get_entry(req.POST['title']) == None:
        util.save_entry(req.POST['title'], req.POST['content'])
        return redirect('encyclopedia:wiki-content', title=req.POST['title'])
    else:
        return render(req, "Error.html", {
            "title": f"Error",
            'errorMsg':  f"Entry named {req.POST['title']} already exists."
        })
    
def editWiki(req, title):
    if req.method == "POST":
        if title != req.POST['title']:
            util.deleteEntry(title)
        util.save_entry(req.POST['title'], req.POST['content'])
        return redirect('encyclopedia:wiki-content', title=req.POST['title'])

    entry = util.get_entry(title)
    if entry == None:
        return render(req, "Error.html", {
            "title": f"{title} Not found.",
            'errorMsg':  f"Entry named {title} does not exists."
        })
    else:
        return render(req, 'encyclopedia/wiki/edit.html', {
            'title': title,
            'markdown': entry
    })

def randomWiki(req):
    entries = util.list_entries()
    if len(entries) == 0:
        return render(req, "Error.html", {
            "title": f"No wiki exists.",
            'errorMsg':  f"No wiki exists."
        })
    index = random.randint(0, len(entries)-1)
    return redirect('encyclopedia:wiki-content', title=entries[index])
