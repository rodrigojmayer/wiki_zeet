import markdown2
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import random
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    found_entry = util.get_entry(entry_name)
    if found_entry != None:
        md = markdown2.Markdown()
        found_entry = md.convert(found_entry)
        return render(request, "encyclopedia/entry.html",{
            "entry_name":entry_name,
            "found_entry":found_entry
        })
    else:
        return render(request, "encyclopedia/not_found.html",{
            "entry_name":entry_name
        })

def search(request):
    entry_search = request.GET.get('q')
    entries = util.list_entries()
    entries_lower = [x.lower() for x in entries]
    matchedEntries = []
    for entry in entries_lower:
        if entry_search.lower() in entry:
            id_matched_entry=entries_lower.index(entry)
            matchedEntries.append(entries[id_matched_entry])
    if (entry_search.lower() in entries_lower):
        found_entry = util.get_entry(entry_search)
        md = markdown2.Markdown()
        found_entry = md.convert(found_entry)
        return render(request, "encyclopedia/entry.html",{
            "entry_name":entry_search,
            "found_entry":found_entry
        })
    elif matchedEntries:
        return render(request, "encyclopedia/not_found.html",{
            "matched":matchedEntries,
            "entry_name":entry_search
        })
    else:
        return render(request, "encyclopedia/not_found.html",{
            "matched":False,
            "entry_name":entry_search
        })

def create(request):
    if (request.method=="GET"):
        if(request.GET.get('create')):
            print(request.GET.get('create'))
            create_title=request.GET.get('create') 
            print(create_title)
            create_title=create_title.lstrip("Create")
            create_title=create_title.lstrip(" ")
            print(create_title)
            return render(request, "encyclopedia/create.html",{
                "entry_name" : create_title
            })
        else:
            return render(request, "encyclopedia/create.html")
    else:
        entries = util.list_entries()
        entries = [x.lower() for x in entries]
        existe=False
        new_title=request.POST["title"].lower()
        for entry in entries:
            if entry == new_title:
                existe=True
        if existe:
            print("Ya existe ese titulo")
            return render(request, "encyclopedia/already_exists.html",{
                "entry_name":new_title
            })
        else:
            content="#"+request.POST["title"]+'\n'+request.POST["content"]
            content=content.encode('utf-8')
            util.save_entry(request.POST["title"], content)
            found_entry = util.get_entry(request.POST["title"])
            md = markdown2.Markdown()
            found_entry = md.convert(found_entry)
            return render(request, "encyclopedia/entry.html",{
                "entry_name" : request.POST["title"],
                "found_entry" : found_entry
            })

def edit(request, entry_name):
    if(request.method=="GET"):
        print(request.GET)
        found_entry = util.get_entry(entry_name)
        return render(request, "encyclopedia/edit.html", {
            "title" : entry_name,
            "content" : found_entry
        })  
    else:
        print(request.POST["title"])
        print(request.POST["content"])
        content=request.POST["content"]
        content=content.encode('utf-8')
        util.save_entry(request.POST["title"], content)
        found_entry = util.get_entry(request.POST["title"])
        md = markdown2.Markdown()
        found_entry = md.convert(found_entry)        
        return render(request, "encyclopedia/entry.html",{
                "entry_name" : request.POST["title"],
                "found_entry" : found_entry
        })  

def random_entry(request):
    entries = util.list_entries()
    entry_random = random.choice(entries)
    found_entry = util.get_entry(entry_random)
    md = markdown2.Markdown()
    found_entry = md.convert(found_entry)        
    return render(request, "encyclopedia/entry.html",{
        "entry_name" : entry_random,
        "found_entry" : found_entry
    })  