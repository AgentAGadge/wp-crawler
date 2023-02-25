"""
    Hyperlist app. service.py for Django framework.
"""
import os
import shutil

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from . import models

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
    # Request the html page to crawl
    request = Request(url)
    html_page = urlopen(request)

    # Parse the html page with BeautifulSoup
    soup_page = BeautifulSoup(html_page, "html.parser")

    # Retrieve all hyperlinks from the BeautifulSoup format of the page
    links = []
    for link in soup_page.findAll('a'):

        link_string = link.get('href')
        if link_string.startswith('/'):
            link_string = url + link_string

        if link.string:
            clickable_text = link.string
            hyperlink = models.create_hyperlink(link_string, url, clickable_text)
        else:
            hyperlink = models.create_hyperlink(link_string, url)

        links.append(hyperlink)

    return links


def update_origin(origin):
    """
    Crawl the URL of an Origin object and store the complete results: hyperlinks, sitemap.

    Parameters 
    ---------- 
        request:
            url: (Origin) Origin object containing the URL to crawl
    Returns
    -------

    """
    # Crawl the URL
    hyperlinks = list_hyperlinks_in(origin.url)
    # Store the results
    store_crawl(origin.url, hyperlinks)


def store_crawl(origin_url, hyperlinks):
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
    # Remove all entries linked to the origin URL
    models.delete_hyperlinks_from_origin(origin_url)
    # Add the results of the last crawl
    models.insert_origin(origin_url)
    models.insert_hyperlinks(hyperlinks)

    # Delete and build storage folder
    stripped_url = origin_url.removeprefix('http://').removeprefix('https://')
    path = os.path.join(PATH_STORAGE, stripped_url)
    # Remove the existing storage for this website, if it exists.
    if os.path.exists(path):
        shutil.rmtree(path)
    # Create storage folder
    os.makedirs(path)
    # Generate and store the sitemap file
    render_context = {'url': origin_url, 'hyperlinks': hyperlinks}
    content = render_to_string('sitemap.html', render_context)
    sitemap_file = open(path+"/"+FILE_NAME_SITEMAP, "w", encoding='utf-8')
    sitemap_file.write(content)
    sitemap_file.close()


def crawl_origins():
    """
    Perform a crawl and stores the results for each Origin object registered in database.
    Parameters 
    ---------- 

    Returns
    -------

    """
    origins = list(models.OriginURL.objects.all())
    for origin in origins:
        update_origin(origin)


def get_stored_crawl_results():
    """
    Retrieves all stored crawl results from the storage folder
    Parameters 
    ---------- 

    Returns
    -------
        crawl_result_list: (List of dicts) Contains all the stored crawl results 
            with the following keys:
                url
                (if the related file exists) sitemap, page.
    """
    crawl_result_list=[]

    #Go through all the stored results
    stored_items = os.scandir(PATH_STORAGE)
    for item in stored_items:
        if item.is_dir():
            crawl_result = {}

            crawl_result_name = item.path.removeprefix(PATH_STORAGE+os.sep)
            crawl_result['url']=crawl_result_name

            sitemap_path = os.path.join(item.path, FILE_NAME_SITEMAP)
            if os.path.isfile(sitemap_path):
                crawl_result['sitemap']=sitemap_path.removeprefix(PATH_STORAGE+os.sep)
                print(sitemap_path)

            crawl_result_list.append(crawl_result)

    return crawl_result_list

def build_server_storage_path(relative_path):
    """
    Build the server path to a file in the storage folder,
    from the relative path starting within storage folder.
    Parameters 
    ---------- 
        relative_path: (String) Relative path from storage folder to the file
    Returns
    -------
        server_path: (String) Absolute path for the server to the file
    """
    server_path = os.path.realpath(os.path.join(PATH_STORAGE, relative_path))
    return server_path
