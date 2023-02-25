"""
    Hyperlist app. admin.py for Django framework.
"""
from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Hyperlink)
class HyperlinkAdmin(admin.ModelAdmin):
    """
        Hyperlink model class for admin view
    """
    list_display = [models.HPLK_CLASS_URL_FIELD, models.HPLK_CLASS_ORIGIN_FIELD,
                    models.HPLK_CLASS_TEXT_FIELD, models.HPLK_CLASS_DATE_DCVR_FIELD]

@admin.register(models.OriginURL)
class OriginURLAdmin(admin.ModelAdmin):
    """
        OriginURL model class for admin view
    """
    list_display = [models.OURL_CLASS_URL_FIELD, models.OURL_CLASS_DATE_FIELD]
