# coding: utf-8
from django.shortcuts import get_object_or_404

from econordeste.core.models import Enterprise, Video, Logo


def enterprise_proc(request):
    """ View Function """
    try:
        enterprise = get_object_or_404(Enterprise, pk=1)
    except:
        enterprise = ''

    video_list = Video.objects.all()[:2]
    logo_list = Logo.objects.all()[:2]

    return {
        'enterprise': enterprise,
        'video_list': video_list,
        'logo_list': logo_list,
    }


class EnterpriseExtraContext(object):
    """ Class Based View """
    try:
        enterprise = get_object_or_404(Enterprise, pk=1)
    except:
        enterprise = ''

    video_list = Video.objects.all()[:2]
    logo_list = Logo.objects.all()[:2]

    extra_context = {
        'enterprise': enterprise,
        'video_list': video_list,
        'logo_list': logo_list,
        }

    def get_context_data(self, **kwargs):
        context = super(EnterpriseExtraContext,
                        self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
