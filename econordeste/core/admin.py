# coding: utf-8
from django.contrib import admin

from mce_filebrowser.admin import MCEFilebrowserAdmin

from econordeste.core.models import (Enterprise, Social, Category, Banner,
                                     Team, Project, Games)
from econordeste.core.forms import TeamForm


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone1', 'phone2', 'phone3', 'email')
    search_fields = ('name', 'description', 'address', 'number', 'complement',
                     'cep', 'district', 'city', 'state',
                     'phone1', 'phone2', 'phone3', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym')
    search_fields = ('name', 'acronym')
    prepopulated_fields = {'slug': ('name',)}


class BannerAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('admin_image', 'title', 'type', 'publish')
    search_fields = ('title',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'admin_image']
    search_fields = ['name', 'description']
    form = TeamForm


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'body')


class GamesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'body')


admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Social)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Games, GamesAdmin)
