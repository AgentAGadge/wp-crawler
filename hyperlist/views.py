from django.shortcuts import render
from django.http import HttpResponse
from . import service

def analyze(request):
    """This call retrieves all the hyperlinks from a url and returns the result in an array on a HTML page.

    Parameters 
    ---------- 
        request:
            url: (String) URL of the page to crawl
    Returns
    -------
        HttpResponse displaying an array with the list of hyperlinks found in the crawled URL.
    
    """
    url_to_crawl = request.GET.get('url')
    hyperlinks = service.list_hyperlinks_in(url_to_crawl)
    return render(request, 'hyperlist.html', { 'hyperlinks': hyperlinks})
