from django.contrib import admin
from models import IttyBittyURL

class IttyBittyURLAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'url', 'date_created', 'hits')
    list_display_links = ('shortcut', 'url')
    search_fields = ('shortcut', 'url')
    list_filter = ('date_created', 'date_updated')
    date_hierarchy = 'date_created'

admin.site.register(IttyBittyURL, IttyBittyURLAdmin)
