# coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from tinymce import models as tinymce_models

from econordeste.current_user import get_current_user


class Calendar(models.Model):
    date_pub = models.DateTimeField(_(u'Data da Publicação'),
                                    auto_now_add=True)
    date_start = models.DateTimeField(_(u'Data de Início'))
    date_end = models.DateTimeField(_(u'Data de Final'))
    created_by = models.ForeignKey(User, verbose_name=u'Criado por',
                                   editable=False, default=get_current_user)
    title = models.CharField(_(u'Título do Evento'), max_length=150)
    slug = models.SlugField(_(u'Link do Evento'), max_length=150,
                            unique=True)
    body = tinymce_models.HTMLField(_(u'Descrição do Evento'))

    def save(self, *args, **kwargs):
        super(Calendar, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse('event:calendar_date_detail',
        #                kwargs={"slug": self.slug})
        return reverse('event:calendar_date_detail',
                       kwargs={'year': self.date_start.year,
                               'month': self.date_start.strftime('%m'),
                               'day': self.date_start.strftime('%d'),
                               'slug': self.slug})

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = _(u'Calendário de Evento')
        verbose_name_plural = _(u'Calendário de Eventos')
        ordering = ['-date_start']
