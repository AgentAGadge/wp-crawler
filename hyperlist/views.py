from django.shortcuts import render
from django.http import HttpResponse
from . import models
from . import service

VPARAM_ANALYZE_URL = 'url'
VPARAM_ANALYZE_STORE = 'url'

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
        #Remove all entries linked to the origin URL
        models.delete_hyperlinks_from_origin(url_to_crawl)
        #Add the results of the last crawl
        models.insert_hyperlinks(hyperlinks)

    #Display the result of the crawl
    return render(request, 'hyperlist.html', { 'hyperlinks': hyperlinks})
