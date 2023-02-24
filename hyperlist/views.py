from django.shortcuts import render
from django.http import HttpResponse
from . import models
from . import service


VPARAM_ANALYZE_URL = 'url'
VPARAM_ANALYZE_STORE = 'store'

def analyze(request):
    """This call retrieves all the hyperlinks from a url and returns the result in an array on a HTML page.

    Parameters 
    ---------- 
        request:
            url: (String) URL of the page to crawl
            store: (String) 'true' to delete and store the hyperlinks, does not impact DB otherwise.
    Returns
    -------
        HttpResponse displaying an array with the list of hyperlinks found in the crawled URL.
    
    """
    #Retrieve parameters
    url_to_crawl = request.GET.get(VPARAM_ANALYZE_URL)
    delete_and_store = request.GET.get(VPARAM_ANALYZE_STORE)

    #Crawl the page for hyperlinks
    hyperlinks = service.list_hyperlinks_in(url_to_crawl)

    #Update the database, if needed
    if('true'==delete_and_store):
        service.storeCrawl(url_to_crawl, hyperlinks)

    #Display the result of the crawl
    render_context = {'url':url_to_crawl, 'hyperlinks': hyperlinks}
    return render(request, 'sitemap.html', render_context)
