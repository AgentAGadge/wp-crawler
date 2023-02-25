"""
    Hyperlist app. forms.py for Django framework.
"""
from django import forms

from . import models

class CreateCrawlForm(forms.Form):
    url = forms.CharField(max_length=200,
                    help_text='Required. URL to crawl (starting with http:// or https://)')

    class Meta:
        model = models.OriginURL
