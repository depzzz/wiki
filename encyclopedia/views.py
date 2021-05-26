from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from . import util
from django import forms
import random
from markdown2 import Markdown

# Global Declaration
markdowner = Markdown()

# Forms
class SearchForm(forms.Form):
    query = forms.CharField(label='Enter Search Query',max_length=100,required=True)

class CreateForm(forms.Form):
    title = forms.CharField(label='Enter Title',max_length=200,required=True)
    content = forms.CharField(label='Enter Content',
                            widget=forms.Textarea,
                            required=True)

class EditForm(forms.Form):
    content = forms.CharField(label='Enter Content',
                            widget=forms.Textarea,
                            required=True)
                            
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "SearchForm": SearchForm
    })

def view(request,entry):
    # check whether the file is in entry folder, if now show error
    if entry.lower() not in (string.lower() for string in util.list_entries()):
        error404 =  "Error 404\nFile Not Found"
        return render(request,"encyclopedia/error.html", {
            "error404" : error404,
            "SearchForm" : SearchForm
        })
    # take user to entry wiki page
    else:
        return render(request, "encyclopedia/view.html", {
            "entry" : markdowner.convert(util.get_entry(entry)),
            "title" : entry,
            "SearchForm" : SearchForm
        })

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = SearchForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            entries = util.list_entries()
            query = form.cleaned_data['query']

            # if query is already present in entries, then take user to query wiki page
            present = [filename for filename in entries if query.lower() in filename.lower()]
            if len(present) == 1 and query.lower() == present[0].lower():
                query = present[0]
                return redirect('view',entry=query)

            # if the query is not present in entries, show user matching search results
            else:
                searchResults = util.Filter(entries,query)
                error404 = "What You're Looking For Ain't Here but here are some results you might be interested in, or Search Again?"
                return render(request, "encyclopedia/error.html",{
                    "error404" : error404,
                    "SearchForm" : SearchForm,
                    "searchResults" : searchResults,
                    "entries" : entries
                })
    # if the request is get then render homepage
    else:
        return render(request, "encyclopedia/index.html", {
            "SearchForm" : SearchForm
        })

def create(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = CreateForm(request.POST)

        # check whether its valid
        if form.is_valid():
            entries = util.list_entries()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # if query is already present in entries, then take user to query wiki page
            present = [filename for filename in entries if title.lower() in filename.lower()]
            if len(present) == 1 and title.lower() == present[0].lower():
                error404 = "You already have this title saved. Rename or Try something else."
                return render(request, "encyclopedia/error.html", {
                    "error404" : error404,
                    "CreateForm" : CreateForm,
                    "SearchForm" : SearchForm
                })
            # Save the Entry
            else:
                save_entry = util.save_entry(title,content)
                return redirect('view',entry=title)
    # render create.html 
    else:
        return render(request, "encyclopedia/create.html", {
            "SearchForm" : SearchForm,
            "CreateForm" : CreateForm
        })

def edit(request,title):
    # render edit page
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "EditForm" : EditForm({"content" : content}),
            "title" : title
        })
    else:
        form = EditForm(request.POST)

        # check whether its valid
        if form.is_valid():
            entries = util.list_entries()
            content = form.cleaned_data['content']

            # if query is already present in entries, then take user to query wiki page
            present = [filename for filename in entries if title.lower() in filename.lower()]
            if len(present) == 1 and title.lower() == present[0].lower():
                util.save_entry(title,content)
                return redirect('view',entry=title)

def random_entry(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)
    content = util.get_entry(randomEntry)

    return render(request, "encyclopedia/view.html", {
        "title" : randomEntry,
        "entry" : markdowner.convert(content),
        "SearchForm" : SearchForm
    })