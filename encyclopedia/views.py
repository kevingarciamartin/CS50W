from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from itertools import groupby
from markdown2 import Markdown
from random import randrange

from . import util

def md_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)

def index(request):
    alphaDict = {}
    entries = util.list_entries()
    for firstLetter, entry in groupby(entries, key=lambda x: x[0]):
        if firstLetter in alphaDict:
            alphaDict[firstLetter] += entry
        else:
            alphaDict[firstLetter] = list(entry)
    return render(request, "encyclopedia/index.html", {
        "alphaDict": alphaDict
    })

def entry(request, title):
    md_content = util.get_entry(title)
    if md_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found"
        })
    else:
        content = md_to_html(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
        
def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        entries = util.list_entries()
        md_content = util.get_entry(query)
        if md_content is not None:
            for entry in entries:
                if query.lower() == entry.lower():
                    return HttpResponseRedirect(reverse("entry", args=[entry]))
        else:
            search_result = []
            for entry in entries:
                if query.lower() in entry.lower():
                    search_result.append(entry)
            alphaDict = {}
            for firstLetter, entry in groupby(search_result, key=lambda x: x[0]):
                if firstLetter in alphaDict:
                    alphaDict[firstLetter] += entry
                else:
                    alphaDict[firstLetter] = list(entry)
            return render(request, "encyclopedia/search_result.html", {
                "alphaDict": alphaDict,
                "query": query
            })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"An encyclopedia entry already exists with the title '{title}'"
            })
        else:
            md_content = request.POST["markdown_content"]
            util.save_entry(title, md_content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method == "POST":
        md_content = request.POST["markdown_content"]
        util.save_entry(title, md_content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
    md_content = util.get_entry(title)    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": md_content
    })
    
def random(request):
    entries = util.list_entries()
    index = randrange(len(entries))
    title = entries[index]
    return HttpResponseRedirect(reverse("entry", args=[title]))