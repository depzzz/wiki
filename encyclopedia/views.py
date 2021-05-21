from django.shortcuts import render
from django.http import HttpResponse
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view(request,entry):
    if entry not in util.list_entries():
        return render(request,"encyclopedia/error.html")
    return render(request, "encyclopedia/view.html", {
        "entry" : util.get_entry(entry),
        "title" : entry
    })
