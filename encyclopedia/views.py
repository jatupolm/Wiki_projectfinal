# Ross P. Coron // 2022-02-22 // CS50W 'Wiki'

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util  # CS50W provided functions
import markdown2    # Text-to-HTML convertor, see: https://github.com/trentm/python-markdown2
import random   # For random page


def index(request):
    """Lists all curent entries"""

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, entry):
    """Renders markdown file in HTML page"""

    # Converts markdown file to string
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/result.html", {
            "message": "404 - Page Not Found (...Literally!)"
        })

    markdown_text = markdown2.markdown(content)
    # markdown_text = markdown2.markdown_path("./entries/" + entry + ".md") - alt. using filepath

    # Renders page, passing in string and page name
    return render(request, "encyclopedia/page.html", {
        "entry": entry,
        "content": markdown_text
    })


def new(request):
    """Creates a new markdown file via an HTML form"""

    if request.method == "GET":
        return render(request, "encyclopedia/new.html")

    # If route accessed via POST (i.e. after submitting form)
    elif request.method == "POST":

        # Stores entry's name and content
        form = request.POST
        title = form['title']
        content = form['content']

        # Checks file does not already exist and renders result (success / fail)
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

    # Get entries, select random, redirect to page passing in name
    entries = util.list_entries()
    page = random.choice(entries)

    return HttpResponseRedirect(reverse("wiki:page", kwargs={'entry': page}))


def search(request):
    """Search for markdown file"""

    if request.method == "POST":
        # Get search term from input
        term = request.POST
        term = term['q']

        entries = util.list_entries()
        page = None

        # Checks for exact match
        for item in entries:
            if term.lower() == item.lower():
                page = item
                print(f"Exact Match Found! -", page)

        # If exact match found, redirect to page
        if page != None:
            return HttpResponseRedirect(reverse("wiki:page", kwargs={'entry': page}))

        # Checks for substring match and appends list
        list = []
        for item in entries:
            if term.lower() in item.lower():
                list.append(item)

        # If no results, render page (Django will catch via {% empty %})
        if not list:
            return render(request, "encyclopedia/results.html")

        # If result(s) found, render as list
        else:
            # Pass into results.html
            return render(request, "encyclopedia/results.html", {
                "results": list
            })

    # I.e. if via GET. Should not be possible but silences Django Error
    else:
        return HttpResponse("Error")
