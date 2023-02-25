"""
    Hyperlist app. views.py for Django framework.
"""
from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from . import service
from . import forms


VPARAM_ANALYZE_URL = 'url'
VPARAM_ANALYZE_STORE = 'store'
VPARAM_DLFILE_PATH = 'file'

class AnalyzeView(LoginRequiredMixin, View):
    """
    This view retrieves all the hyperlinks from a url 
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
        #Retrieve parameters
        url_to_crawl = request.GET.get(VPARAM_ANALYZE_URL)
        delete_and_store = request.GET.get(VPARAM_ANALYZE_STORE)

        #Crawl the page for hyperlinks
        hyperlinks = service.list_hyperlinks_in(url_to_crawl)

        #Update the database, if needed
        if 'true'==delete_and_store:
            service.store_crawl(url_to_crawl, hyperlinks)

        #Display the result of the crawl
        context = {'url':url_to_crawl, 'hyperlinks': hyperlinks}
        return render(request, 'sitemap.html', context)

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
            #Crawl the page for hyperlinks
            hyperlinks = service.list_hyperlinks_in(url)
            #Update the database
            service.store_crawl(url, hyperlinks)
            print('toto')
            context['crawl_result']= {"url": url, "hyperlinks": hyperlinks}

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
