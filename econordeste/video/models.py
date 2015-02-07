# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class VideoEntry(models.Model):
    title = models.CharField(_(u'Video'), max_length=100)
    body = models.TextField(_(u'Descrição'), blank=True, null=True)
    url = models.URLField(_(u'Endereço do Vídeo'))

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = _(u'Vídeo')
        verbose_name_plural = _(u'Vídeos')
