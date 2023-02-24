from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from . import models
import os
import shutil
from django.template.loader import render_to_string

PATH_STORAGE = 'storage'
FILE_NAME_SITEMAP = 'sitemap.html'

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
        linkString = link.get('href')
        clickableText = link.string #TODO
        if linkString.startswith('/'):
            linkString = url + linkString 
        hyperlink = models.Hyperlink.create(linkString, url, clickableText)
        links.append(hyperlink)

    return links

def updateOrigin(origin):
    """
    Crawl the URL of an Origin object and store the complete results: hyperlinks, sitemap.

    Parameters 
    ---------- 
        request:
            url: (Origin) Origin object containing the URL to crawl
    Returns
    -------
    
    """
    #Crawl the URL
    hyperlinks = list_hyperlinks_in(origin.url)
    #Store the results
    storeCrawl(origin.url, hyperlinks)

def storeCrawl(originUrl,hyperlinks):
    """
    Stores complete results of a crawl: hyperlinks, sitemap and origin.

    Parameters 
    ---------- 
        request:
            originUrl: (String) URL that was crawled
            hyperlinks: (List of Hyperlinks) hyperlinks returned by the crawl
    Returns
    -------
    
    """
    #Remove all entries linked to the origin URL
    models.delete_hyperlinks_from_origin(originUrl)
    #Add the results of the last crawl
    models.insert_origin(originUrl)
    models.insert_hyperlinks(hyperlinks)

    #Delete and build storage folder
    strippedUrl = originUrl.removeprefix('http://').removeprefix('https://')
    path = os.path.join(PATH_STORAGE, strippedUrl)
    #Remove the existing storage for this website, if it exists.
    if os.path.exists(path): 
        shutil.rmtree(path)
    #Create storage folder
    os.makedirs(path)
    #Generate and store the sitemap file
    render_context = {'url':originUrl, 'hyperlinks': hyperlinks}
    content = render_to_string('sitemap.html', render_context)            
    f = open(path+"/"+FILE_NAME_SITEMAP, "w")
    f.write(content)
    f.close()

def crawlOrigins():
    """
    Perform a crawl and stores the results for each Origin object registered in database.
    Parameters 
    ---------- 

    Returns
    -------
    
    """
    origins = list(models.OriginURL.objects.all())
    for origin in origins:
        updateOrigin(origin)

