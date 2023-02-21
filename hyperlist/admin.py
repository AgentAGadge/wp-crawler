from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Hyperlink)
class HyperlinkAdmin(admin.ModelAdmin):
    list_display = [models.HPLK_CLASS_URL_FIELD, models.HPLK_CLASS_ORIGIN_FIELD, models.HPLK_CLASS_DATE_DCVR_FIELD]

    #Remove UI to add/change/delete table
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(models.OriginURL)
class OriginURLAdmin(admin.ModelAdmin):
    list_display = [models.OURL_CLASS_URL_FIELD, models.OURL_CLASS_DATE_FIELD]