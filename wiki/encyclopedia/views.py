from django.shortcuts import render
from markdown2 import Markdown

from . import util

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
        
def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        content = md_to_html(query)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
            })
        else:
            search_result = []
            entries = util.list_entries()
            for entry in entries:
                if query.lower() in entry.lower():
                    search_result.append(entry)
            return render(request, "encyclopedia/search_result.html", {
                "query": query,
                "search_result": search_result
            })
