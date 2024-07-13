from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
markdowner = Markdown()
from django import forms
import random as ran
from math import floor

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "cols":"5"}))
class EditForm(forms.Form):
    title = forms.CharField(widget = forms.HiddenInput())
    content = forms.CharField(widget=forms.Textarea())

from . import util, myutil


def index(request):
    if request.method == "POST":
        entries = []
        items = util.list_entries()
        for item in items:
            if item.lower() == request.POST["q"].lower():
                return HttpResponseRedirect(f"wiki/{item}")
            print(item.lower().find(request.POST['q'].lower()) != -1)
            if item.lower().find(request.POST['q'].lower()) != -1:
                entries.append(item)
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "search": True,
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": False,
    })

def page(request, page):   
    md = util.get_entry(page)
    if not md == None:
        content = {
            "pagecontent": myutil.convertToHtml(md),
            "title": page
        }
        try:
            if request.GET["success"] == "create":
                content["type"] = "success"
                content["message"] = "new entry added successfully"
            elif request.GET["success"] == "edit":
                content["type"] = "success"
                content["message"] = "entry edited successfully"

        except:
            pass
        myutil.convertToHtml(md)
        return render(request, "encyclopedia/page.html",content)
    else:
        return render(request, "encyclopedia/page.html",{
            "pagecontent": f"<h1>'{page}' does not exist!</h1>",
        })

def random(request):
    pages = util.list_entries()
    total = len(pages)
    number = floor(ran.random() * total)
    return HttpResponseRedirect(f"/wiki/{pages[number]}")

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            if not util.get_entry(data["title"].capitalize()):
                util.save_entry(data["title"].capitalize(), data["content"])
                return HttpResponseRedirect(f"/wiki/{data["title"]}?success=create")
            else:
                return render(request, "encyclopedia/form.html", {
                    "new":True,
                    "type": "error",
                    "message": "this page already exists, please edit the original form, or use a different title",
                    "form":form,
                })
        else:
            return render(request, "encyclopedia/form.html", {
                "new":True,
                "type": "error",
                "message": "form data is not valid",
                "form":form,
            })

    return render(request, "encyclopedia/form.html", {
        "new":True,
        "form":NewEntryForm,
    })

def edit(request, page):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"].encode()
            title = form.cleaned_data["title"]
            print(request.POST["title"])
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}?success=edit")
    content = util.get_entry(page)
    return render(request, "encyclopedia/form.html",{
                "new": False,
                "title": page,
                "form": EditForm({"title": page, "content": content}) 
    })