# coding: utf-8
from django.db.models import Q
from django.views import generic
from django.views.generic.dates import (YearArchiveView, MonthArchiveView,
                                        DayArchiveView)

from econordeste.context_processors import EnterpriseExtraContext

from econordeste.event.models import Calendar


class CalendarYearArchiveView(YearArchiveView):
    # queryset = Entry.objects.filter(is_active=True,
    #                                 kind='A').order_by('-pub_date', 'title')
    queryset = Calendar.objects.all()
    date_field = "date_start"
    make_object_list = True
    allow_future = True
    # TODO: mudar a paginacao
    paginate_by = 20

    # def get_queryset(self):
    #     return Calendar.objects.filter(date_start__year=self.get_year())


class CalendarMonthArchiveView(MonthArchiveView):
    queryset = Calendar.objects.all()
    date_field = "date_start"
    make_object_list = True
    allow_future = True


class CalendarDayArchiveView(DayArchiveView):
    queryset = Calendar.objects.all()
    date_field = "date_start"
    make_object_list = True
    allow_future = True


class CalendarListView(EnterpriseExtraContext, generic.ListView):
    model = Calendar
    template_name = 'event/calendar_home.html'
    # TODO: mudar a paginacao
    paginate_by = 20

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        if search:
            obj_lst = Calendar.objects.filter(Q(title__icontains=search) |
                                              Q(date_start__icontains=search) |
                                              Q(body__icontains=search))
        else:
            obj_lst = Calendar.objects.all()
        return obj_lst

    def get_context_data(self, **kwargs):
        context = super(CalendarListView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        return context


class CalendarDateDetailView(EnterpriseExtraContext, generic.DateDetailView):
    model = Calendar
    date_field = 'date_start'
    make_object_list = True
    allow_future = True
