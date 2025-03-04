

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util  
import markdown2    
import random  

def index(request):
    """Lists all curent entries"""

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, entry):
    """Renders markdown file in HTML page"""

    
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/result.html", {
            "message": "404 - Page Not Found (...Literally!)"
        })

    markdown_text = markdown2.markdown(content)
   
    return render(request, "encyclopedia/page.html", {
        "entry": entry,
        "content": markdown_text
    })


def new(request):
    """Creates a new markdown file via an HTML form"""

    if request.method == "GET":
        return render(request, "encyclopedia/new.html")

    
    elif request.method == "POST":

        
        form = request.POST
        title = form['title']
        content = form['content']

        
        entries = util.list_entries()

        print(title)
        print(entries)

        for item in entries:
            if title.lower() == item.lower():
                return render(request, "encyclopedia/result.html", {
                    "message": "Error! New entry was NOT added."
                })

        util.save_entry(title, content)
        return render(request, "encyclopedia/result.html", {
            "message": "Success! New entry added."
        })


def edit(request, entry):
    """Edit markdown file via HTML form"""

    if request.method == "GET":

        content = util.get_entry(entry)

        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "content": content,
        })

    elif request.method == "POST":

        form = request.POST
        title = form['title']
        content = form['content']

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki:page", kwargs={'entry': title}))


def random_page(request):
    """Display random entry"""

    
    entries = util.list_entries()
    page = random.choice(entries)

    return HttpResponseRedirect(reverse("wiki:page", kwargs={'entry': page}))


def search(request):
    """Search for markdown file"""

    if request.method == "POST":
        
        term = request.POST
        term = term['q']

        entries = util.list_entries()
        page = None

       
        for item in entries:
            if term.lower() == item.lower():
                page = item
                print(f"Exact Match Found! -", page)

        
        if page != None:
            return HttpResponseRedirect(reverse("wiki:page", kwargs={'entry': page}))

        
        list = []
        for item in entries:
            if term.lower() in item.lower():
                list.append(item)

       
        if not list:
            return render(request, "encyclopedia/results.html")

        
        else:
           
            return render(request, "encyclopedia/results.html", {
                "results": list
            })

   
    else:
        return HttpResponse("Error")
