from django.shortcuts import render
from markdown2 import Markdown
markdowner = Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, page):   
    md = util.get_entry(page)
    if not md == None:
        html = markdowner.convert(md)
        return render(request, "encyclopedia/page.html",{
            "pagecontent": html,
        })
    else:
        return render(request, "encyclopedia/page.html",{
            "pagecontent": f"<h1>'{page}' does not exist!</h1>",
        })
