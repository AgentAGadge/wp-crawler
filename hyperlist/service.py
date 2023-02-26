"""
    Hyperlist app. service.py for Django framework.
"""
import os
import shutil

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from . import models

PATH_STORAGE = 'storage'
FILE_NAME_SITEMAP = 'sitemap.html'
FILE_NAME_HTMLPAGE = 'page.html'

def get_soup_from_url(url):
    """
    This function retrieves the HTML from a URL

    Parameters 
    ---------- 
        url: (String) URL to open to retrieve the HTML of interest.
    Returns
    -------
        soup_page: (BeautifulSoup) Returned HTTPResponse as parsed HTML

    """
    # Request the html page to crawl
    request = Request(url)
    http_response = urlopen(request)
    # Parse the html page with BeautifulSoup
    soup_page = BeautifulSoup(http_response, "html.parser")
    return soup_page

def list_hyperlinks_in(soup_page, url):
    """
    This function retrieves all the hyperlinks from a url and returns the list.

    Parameters 
    ---------- 
        soup_page: (BeautifulSoup) HTML page to crawl, returned from get_soup_from_url
    Returns
    -------
        links: (list of hyperlink) All hyperlinks found in the URL to crawl.

    """
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


def crawl(url):
    """
    Crawl the URL of an Origin object and store the complete results: hyperlinks, sitemap.

    Parameters 
    ---------- 
        url: (Origin) Origin object containing the URL to crawl
    Returns
    -------
        hyperlinks: (List of Hyperlinks) hyperlinks found in the url
    """
    #Retrieve the HTML page as soup object from the URL
    soup_page = get_soup_from_url(url)
    # Crawl the page
    hyperlinks = list_hyperlinks_in(soup_page, url)
    # Store the results
    store_crawl(url, hyperlinks, soup_page)

    return hyperlinks


def store_crawl(origin_url, hyperlinks, soup_page):
    """
    Stores complete results of a crawl: hyperlinks, sitemap, HTML page and origin.

    Parameters 
    ---------- 
        origin_url: (String) URL that was crawled
        hyperlinks: (List of Hyperlinks) hyperlinks returned by the crawl
        soup_page: (BeautifulSoup) HTML page returned from the URL as soup object
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
    #Store the HTML page
    html_page = soup_page.prettify( formatter="html" )
    html_file = open(path+"/"+FILE_NAME_HTMLPAGE, "w", encoding='utf-8')
    html_file.write(html_page) 
    html_file.close()
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
        crawl(origin.url)


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
            page_path = os.path.join(item.path, FILE_NAME_HTMLPAGE)
            if os.path.isfile(page_path):
                crawl_result['page']=page_path.removeprefix(PATH_STORAGE+os.sep)

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
