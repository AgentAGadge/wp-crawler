"""
    Hyperlist app. views.py for Django framework.
"""
from urllib.error import URLError, HTTPError

from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from . import service
from . import forms


VPARAM_ANALYZE_URL = 'url'
VPARAM_ANALYZE_STORE = 'store'
VPARAM_DLFILE_PATH = 'file'

class HomeView(LoginRequiredMixin,View):
    """
    This call retrieves all the hyperlinks from a url 
    and returns the result in an array on a HTML page.

    Parameters 
    ---------- 
        request:
            url: (String) URL of the page to crawl
            store: (String) 'true' to delete and store the hyperlinks, does not impact DB otherwise.
    Returns
    -------
        HttpResponse displaying an array with the list of hyperlinks found in the crawled URL.
    
    """
    def get(self, request):
        """GET"""
        context = {}

        #Manage the Crawl creation form
        form = forms.CreateCrawlForm()
        context['create_crawl_form'] = form

        #Manage the list of existing crawl results
        crawl_results=service.get_stored_crawl_results()
        context['stored_results'] = crawl_results

        return render(request, "home.html", context)

    def post(self, request):
        """POST"""
        context = {}
        #Manage the Crawl creation form and results
        form = forms.CreateCrawlForm(request.POST)
        if form.is_valid():
            #Retrieve URL from the form
            url = form.cleaned_data.get('url')
            try:
                hyperlinks = service.crawl(url)
                context['crawl_result']= {"url": url, "hyperlinks": hyperlinks}
            except HTTPError as error:
                context['crawl_error']="""The HTTP response is incorrect.
                 Make sure you can access the targeted URL.""" + str(error)
            except URLError as error:
                context['crawl_error']="""The URL cannot be reached.
                Make sure you can access the targeted URL.""" + str(error)
            except OSError as error:
                context['crawl_error']="""Internal server issue to store the results.
                  Please retry. If the issue remains, contact the server manager.""" + str(error)
            except ValueError as error:
                context['crawl_error']="""An unexpected value was received.
                  Make sure you entered a correct URL.
                  Otherwise, contact the server manager.""" + str(error)
            except Exception as error:
                context['crawl_error']="""An unknown error occured.
                 Please contact the server manager.""" + str(error)
        context['create_crawl_form'] = form

        #Manage the list of existing crawl results
        crawl_results=service.get_stored_crawl_results()
        context['stored_results'] = crawl_results

        return render(request, "home.html", context)

class DownloadStorageFileView(LoginRequiredMixin, View):
    """
    This call starts the download of the file identified with
    its relative path from storage folder on the server

    Parameters 
    ---------- 
        request:
            file: (String) Relative path to the file from storage folder.
    Returns
    -------
        response: (FileResponse) Download the file.
    
    """
    def get(self, request):
        """GET"""
        relative_path = request.GET.get(VPARAM_DLFILE_PATH)
        server_path = service.build_server_storage_path(relative_path)
        response = FileResponse(open(server_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="'+relative_path+'"'
        return response
