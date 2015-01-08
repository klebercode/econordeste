# coding: utf-8
from django.contrib import admin

from mce_filebrowser.admin import MCEFilebrowserAdmin

from econordeste.blog.models import Entry


class EntryAdmin(MCEFilebrowserAdmin):
    list_filter = ('created', 'author__username', 'tags',
                   'categories')
    list_display = ('title', 'created', 'author', 'publish')
    search_fields = ('title', 'created', 'author', 'body')
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Entry, EntryAdmin)
