"""
    Hyperlist app. models.py for Django framework.
"""
from django.db import models


# Create your models here.

# ORIGINURL CONSTANT DEFINITION
OURL_CLASS_URL_FIELD = "url"
OURL_CLASS_DATE_FIELD = "date_created"
class OriginURL(models.Model):
    """
       OriginURL model registers URL that have been crawled and that have scheduled crawls.
    """
    #url link found
    url = models.CharField(max_length = 200)
    #DateTime of the hyperlink entry creation
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.url)

def create_origin_url(url):
    """
    This function creates a Origin object with a URL and returns it.
    Parameters 
    ---------- 
        url: (String) url link of the Hyperlink object to create
    Returns
    -------
        (OriginURL) Created object
    """
    origin = OriginURL()
    origin.url = url
    return origin

def insert_origin(origin_url):
    """
    Create a OriginURL object in database from a URL if it does not exist already.
    Parameters 
    ---------- 
        origin_url: (String) URL to associate to the Origin object
    Returns
    -------
        origin: (OriginURL) created or already existing OriginURL object.
    
    """
    #Search for a matching already existing OriginURL.
    origin_list = list(OriginURL.objects.filter(url=origin_url))
    #If it does not exist, create and insert.
    if 0==len(origin_list):
        origin = create_origin_url(origin_url)
        origin.save()
    else: #Otherwise, retrieve it.
        origin = origin_list[0]
    return origin


# HYPERLINK CONSTANT DEFINITION
HPLK_CLASS_URL_FIELD = "url"
HPLK_CLASS_ORIGIN_FIELD = "origin"
HPLK_CLASS_TEXT_FIELD = "text"
HPLK_CLASS_DATE_DCVR_FIELD = "date_discovered"
class Hyperlink(models.Model):
    """
       Hyperlink model registers hyperlinks found in OriginURL pages.
    """
    #url link found
    url = models.CharField(max_length = 200)
    #url link of the origin page on which the Hyperlink has been found
    origin = models.CharField(max_length = 200)
    #Human-readable string to display the hyperlink
    text = models.CharField(max_length = 200)
    #DateTime of the hyperlink entry creation
    date_discovered = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.url

def create_hyperlink(url, origin, text=''):
    """
    This function creates a Hyperlink object with url and origin, and returns it.
    Parameters 
    ---------- 
        url: (String) url link of the Hyperlink object to create
        origin: (String) url link of the origin page on which the Hyperlink has been found
        text: (String - Optional) clickable text associated to the hyperlink. If not provided, url is used.
    Returns
    -------
        (Hyperlink) Created object
    """
    hyperlink = Hyperlink()
    hyperlink.url = url
    hyperlink.origin = origin
    if ''==text:
        hyperlink.text = url
    else:
        hyperlink.text = text
    return hyperlink

def insert_hyperlinks(hyperlinks):
    """
    This function inserts in DB a list of hyperlinks.

    Parameters 
    ---------- 
        hyperlinks: (List of hyperlinks) List of hyperlinks to store in DB.
    Returns
    -------
    
    """
    for hyperlink in hyperlinks:
        hyperlink.save()

def delete_hyperlinks_from_origin(origin):
    """
    This function removes all hyperlinks in DB with a given 
    Parameters 
    ---------- 
        origin: (String) value of origin column for which all hyperlink entries must be deleted.
    Returns
    -------
    
    """
    hyperlinks = list(Hyperlink.objects.filter(origin=origin))
    for hyperlink in hyperlinks:
        hyperlink.delete()
