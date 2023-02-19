from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import randint

def convert_markdown(title):
    page = util.get_entry(title)
    markdowner = Markdown()
    if page == None:
        return None
    else:
        return markdowner.convert(page)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page_render(request, title):
    page_html = util.get_entry(title)

    if page_html == None:
        return render(request, 'encyclopedia/error.html',{
            'error' : 'Page not Found'
        })
    else:
        return render(request, 'encyclopedia/entry-page.html',{
            'title' : title,
            'page_html' : convert_markdown(title)
        })
    
def search(request):
    if request.method == 'POST':
        search_string = request.POST['q'].lower()

        if util.get_entry(search_string) == None:
            all_entries = util.list_entries()
            results = []
            for entry in all_entries:
                if search_string in entry.lower():
                    results.append(entry)
            return render(request, 'encyclopedia/search-results.html', {
                'results': results
            })
        else:
            return page_render(request, search_string)
        
def render_create_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/create-page.html')
    else:
        page_title = request.POST['title']
        page_md = request.POST['pmarkdown']
        title_check = util.get_entry(page_title)
        
        if title_check != None:
            return render(request, 'encyclopedia/error.html', {
                'error' : 'Page already exists'
            })
        else:
            util.save_entry(page_title, page_md)
            return render(request, 'encyclopedia/entry-page.html', {
                'title' : page_title,
                'page_html' : page_md
            })
        
def edit_page(request):
        original_title = request.POST['ptitle']
        original_md = util.get_entry(original_title)
        return render(request, 'encyclopedia/edit.html', {
            'original_title' : original_title,
            'original_md' : original_md
        })

def edit_submit(request):
    if request.method == 'POST':
        edited_title = request.POST['edited_title']
        edited_md = request.POST['edited_md']
        util.save_entry(edited_title, edited_md)
        return render(request, 'encyclopedia/entry-page.html', {
            'title' : edited_title,
            'page_html' : convert_markdown(edited_title)
        })

def random(request):
    random_entry = []
    all_entries = util.list_entries()
    for entry in all_entries:
        random_entry.append(entry)

    random_index = randint(0, len(random_entry) - 1)

    return page_render(request, random_entry[random_index])
    



