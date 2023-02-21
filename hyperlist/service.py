from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from . import models

def list_hyperlinks_in(url):
    """
    This function retrieves all the hyperlinks from a url and returns the list.

    Parameters 
    ---------- 
        url: (String) URL of the page to crawl
    Returns
    -------
        links: (list of hyperlink) All hyperlinks found in the URL to crawl.
    
    """
    #Request the html page to crawl
    request = Request(url)
    html_page = urlopen(request)

    #Parse the html page with BeautifulSoup
    soup_page = BeautifulSoup(html_page, "html.parser")

    #Retrieve all hyperlinks from the BeautifulSoup format of the page
    links = []
    for link in soup_page.findAll('a'):
        hyperlink = models.Hyperlink.create(link.get('href'), url)
        links.append(hyperlink)

    return links

def updateOrigin(origin):
    hyperlinks = list_hyperlinks_in(origin.url)
    models.delete_hyperlinks_from_origin(origin.url)
    models.insert_hyperlinks(hyperlinks)

def crawlOrigins():
    origins = list(models.OriginURL.objects.all())
    for origin in origins:
        updateOrigin(origin)

