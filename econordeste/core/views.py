# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import RequestContext

from econordeste.context_processors import enterprise_proc

from econordeste.core.models import Banner, Team, Project, Games
from econordeste.blog.models import Entry

from econordeste.core.forms import ContactForm


def home(request):
    context = {}
    context['blog_list'] = Entry.published.all()[:16]
    context['super_banner_list'] = Banner.published.filter(type=1)
    context['second_banner_list'] = Banner.published.filter(type=2)
    context['popup_banner_list'] = Banner.published.filter(type=3)[:1]

    return render(request, 'home.html', context,
                  context_instance=RequestContext(request,
                                                  processors=[enterprise_proc]
                                                  ))


def contact(request):
    context = {}

    # contact
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            context['contact_success'] = True
    else:
        form = ContactForm()

    context['contact_form'] = form

    return render(request, 'contact.html', context,
                  context_instance=RequestContext(request,
                                                  processors=[enterprise_proc]
                                                  ))


def soundcloud(request):
    context = {}

    pagina = request.GET.get('pagina', '')
    if pagina:
        context['pagina'] = pagina

    return render(request, 'radio.html', context)
    # return redirect('http://saloa.pe.gov.br/transparencia/')


def team(request):
    context = {}
    context['team_list'] = Team.objects.all()

    return render(request, 'team.html', context,
                  context_instance=RequestContext(request,
                                                  processors=[enterprise_proc]
                                                  ))


def project(request):
    context = {}
    context['project_list'] = Project.objects.all()

    return render(request, 'project.html', context,
                  context_instance=RequestContext(request,
                                                  processors=[enterprise_proc]
                                                  ))


def games(request):
    context = {}
    context['games_list'] = Games.objects.all()

    return render(request, 'games.html', context,
                  context_instance=RequestContext(request,
                                                  processors=[enterprise_proc]
                                                  ))
