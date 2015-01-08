# coding: utf-8
from django import forms
from tinymce.widgets import TinyMCE

from econordeste.event.models import Calendar


class CalendarModelForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(
                           attrs={'cols': 100, 'rows': 50}))

    class Meta:
        model = Calendar
