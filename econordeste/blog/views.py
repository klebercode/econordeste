# coding: utf-8
from django.db.models import Q
from django.views import generic
from django.views.generic.dates import (YearArchiveView, MonthArchiveView,
                                        DayArchiveView)

from econordeste.context_processors import EnterpriseExtraContext

from econordeste.blog.models import Entry
from econordeste.core.models import Category


class EntryYearArchiveView(YearArchiveView):
    queryset = Entry.published.all()
    date_field = 'created'
    make_object_list = True
    allow_future = True
    # TODO: mudar a paginacao
    paginate_by = 10


class EntryMonthArchiveView(MonthArchiveView):
    queryset = Entry.published.all()
    date_field = 'created'
    make_object_list = True
    allow_future = True


class EntryDayArchiveView(DayArchiveView):
    queryset = Entry.published.all()
    date_field = 'created'
    make_object_list = True
    allow_future = True


class EntryListView(EnterpriseExtraContext,  generic.ListView):
    # model = Entry
    queryset = Entry.published.all()
    template_name = 'blog/entry_home.html'
    # TODO: mudar a paginacao
    paginate_by = 10

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        if search:
            obj_lst = Entry.published.filter(Q(title__icontains=search) |
                                             Q(created__icontains=search) |
                                             Q(body__icontains=search))
        else:
            obj_lst = Entry.published.all()
        return obj_lst

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['search'] = search
        context['tag_list'] = Entry.tags.most_common()
        # TODO: mudar a forma de carregamento das categorias
        context['category_list'] = Category.objects.all().order_by('?')[:10]
        return context


class EntryDateDetailView(EnterpriseExtraContext, generic.DateDetailView):
    # model = Entry
    queryset = Entry.published.all()
    date_field = 'created'
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(EntryDateDetailView, self).get_context_data(**kwargs)
        context['tag_list'] = Entry.tags.most_common()
        # TODO: mudar a forma de carregamento das categorias
        context['category_list'] = Category.objects.all().order_by('?')[:10]
        return context


class EntryTagListView(EntryListView):
    """
    Herda de EntryListView mudando o filtro para tag selecionada
    """
    def get_queryset(self):
        """
        Incluir apenas as Entries marcadas com a tag selecionada
        """
        return Entry.published.filter(tags__slug=self.kwargs['tag_slug'])


class EntryCategoryListView(EntryListView):
    """
    Herda de EntryListView mudando o filtro para categoria selecionada
    """
    def get_queryset(self, **kwargs):
        """
        Inclui apenas as Entries marcadas com a categoria selecionada
        """
        return Entry.published.filter(categories__slug=self.kwargs['cat_slug'])
