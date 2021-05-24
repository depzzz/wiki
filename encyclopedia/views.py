from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from . import util
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Enter Search Query',max_length=100,required=True)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "SearchForm": SearchForm
    })

def view(request,entry):
    if entry.lower() not in (string.lower() for string in util.list_entries()):
        error404 =  "Error 404\nFile Not Found"
        return render(request,"encyclopedia/error.html", {
            "error404" : error404,
            "SearchForm" : SearchForm
        })
    else:
        return render(request, "encyclopedia/view.html", {
            "entry" : util.get_entry(entry),
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
            present = [filename for filename in entries if query.lower() in filename.lower()]
            if len(present) == 1 and query.lower() == present[0].lower():
                query = present[0]
                return redirect('view',entry=query)
            else:
                searchResults = util.Filter(entries,query)
                error404 = "What You're Looking For Ain't Here but here are some results you might be interested in, or Search Again?"
                return render(request, "encyclopedia/error.html",{
                    "error404" : error404,
                    "SearchForm" : SearchForm,
                    "searchResults" : searchResults,
                    "entries" : entries
                })
    else:
        render(request, "encyclopedia/index.html", {
            "SearchForm" : SearchForm
        })