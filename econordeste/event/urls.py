# coding: utf-8
from django.conf.urls import patterns, url

from econordeste.event.views import (CalendarYearArchiveView,
                                     CalendarMonthArchiveView,
                                     CalendarDayArchiveView,
                                     CalendarListView,
                                     CalendarDateDetailView)


urlpatterns = patterns(
    'econordeste.event.views',
    url(r'^$', CalendarListView.as_view(), name='home'),
    url(r'^(?P<year>\d{4})/$',
        CalendarYearArchiveView.as_view(),
        name='calendar_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/$',
        CalendarMonthArchiveView.as_view(month_format='%m'),
        name='calendar_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$',
        CalendarDayArchiveView.as_view(month_format='%m'),
        name='calendar_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[-\w]+)/$',
        CalendarDateDetailView.as_view(month_format='%m'),
        name='calendar_date_detail'),
)
