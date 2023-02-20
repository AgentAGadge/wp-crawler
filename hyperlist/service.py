from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from . import models

def list_hyperlinks_in(url):
    request = Request(url)
    html_page = urlopen(request)

    soup_page = BeautifulSoup(html_page, "html.parser")

    links = []
    for link in soup_page.findAll('a'):
        hyperlink = models.hyperlink(link.get('href'), url)
        links.append(hyperlink)

    return links
    