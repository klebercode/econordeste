# coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

import uuid
import os

from sorl.thumbnail import ImageField
from tinymce import models as tinymce_models

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps


STATE_CHOICES = (
    ('AC', u'Acre'),
    ('AL', u'Alagoas'),
    ('AP', u'Amapá'),
    ('AM', u'Amazonas'),
    ('BA', u'Bahia'),
    ('CE', u'Ceará'),
    ('DF', u'Distrito Federal'),
    ('ES', u'Espírito Santo'),
    ('GO', u'Goiás'),
    ('MA', u'Maranhão'),
    ('MT', u'Mato Grosso'),
    ('MS', u'Mato Grosso do Sul'),
    ('MG', u'Minas Gerais'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PR', u'Paraná'),
    ('PE', u'Pernambuco'),
    ('PI', u'Piauí'),
    ('RJ', u'Rio de Janeiro'),
    ('RN', u'Rio Grande do Norte'),
    ('RS', u'Rio Grande do Sul'),
    ('RO', u'Rondônia'),
    ('RR', u'Roraima'),
    ('SC', u'Santa Catarina'),
    ('SP', u'São Paulo'),
    ('SE', u'Sergipe'),
    ('TO', u'Tocantins'),
)

BANNER_CHOICES = (
    (1, _(u'Super Banner (Home)')),
    # (2, _(u'Banner Secundário (Home)')),
    (3, _(u'Popup Banner')),
)


class Social(models.Model):
    name = models.CharField(_(u'Nome'), max_length=50,
                            help_text='Ex: Facebook')
    link = models.URLField(_(u'Link'),
                           help_text='Ex: http://www.facebook.com/usuario')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u'Mídia Social')
        verbose_name_plural = _(u'Mídias Sociais')
        ordering = ['name']


class Enterprise(models.Model):
    name = models.CharField(_(u'Nome'), max_length=100)
    description = models.CharField(_(u'Descrição'), max_length=100,
                                   blank=True, null=True)
    cnpj = models.CharField(_(u'CNPJ'), max_length=20,
                            help_text='99.999.999/9999-99')
    address = models.CharField(_(u'Endereço'), max_length=200)
    number = models.CharField(_(u'Número'), max_length=10)
    complement = models.CharField(_(u'Complemento'), max_length=100,
                                  blank=True, null=True)
    cep = models.CharField(_(u'CEP'), max_length=9, help_text='99999-999',
                           blank=True, null=True)
    district = models.CharField(_(u'Bairro'), max_length=100)
    city = models.CharField(_(u'Cidade'), max_length=100)
    state = models.CharField(_(u'UF'), max_length=2, choices=STATE_CHOICES)
    country = models.CharField(_(u'País'), max_length=50)
    phone1 = models.CharField(_(u'Fone 1'), max_length=20,
                              help_text='(99) 9999-9999')
    phone2 = models.CharField(_(u'Fone 2'), max_length=20,
                              help_text='(99) 9999-9999', blank=True,
                              null=True)
    phone3 = models.CharField(_(u'Fone 3 (Fax)'), max_length=20,
                              help_text='(99) 9999-9999', blank=True,
                              null=True)
    email = models.EmailField(_(u'Email'))
    site = models.URLField(_(u'Site'))
    socials = models.ManyToManyField('Social',
                                     verbose_name=_(u'Mídias Sociais'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u'Empresa')
        verbose_name_plural = _(u'Empresa')


class Category(models.Model):
    name = models.CharField(_(u'Nome da Categoria'), max_length=200)
    slug = models.SlugField(_(u'Link no Site'), max_length=200,
                            unique=True)
    acronym = models.CharField(_(u'Sigla'), max_length=50, blank=True,
                               null=True)

    def get_absolute_url(self):
        return reverse('blog:category_list', kwargs={'pk': self.pk})

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u'Categoria')
        verbose_name_plural = _(u'Categorias')
        ordering = ['name']


class BannerManager(models.Manager):
    def get_queryset(self):
        return super(BannerManager,
                     self).get_queryset().all()


class BannerPublishedManager(models.Manager):
    def get_queryset(self):
        return super(BannerPublishedManager,
                     self).get_queryset().filter(publish=True)


class Banner(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('banner', filename)

    type = models.IntegerField(_(u'Banner'), choices=BANNER_CHOICES, default=1)
    image = ImageField(_(u'Banner'), upload_to=get_file_path)
    title = models.CharField(_(u'Título do banner'), max_length=100)
    link = models.URLField(_(u'Link do banner'), blank=True, null=True)
    publish = models.BooleanField(_(u'Visível no site?'), default=True)

    objects = BannerManager()
    published = BannerPublishedManager()

    def admin_image(self):
        return '<img src="%s" width="200" />' % self.image.url
    admin_image.allow_tags = True
    admin_image.short_description = 'Imagem'

    def save(self, *args, **kwargs):
        if not self.id and not self.image:
            return

        super(Banner, self).save(*args, **kwargs)

        image = Image.open(self.image)

        def scale_dimensions(width, height, longest_side):
            if width > height:
                if width > longest_side:
                    ratio = longest_side*1./width
                    return (int(width*ratio), int(height*ratio))
                elif height > longest_side:
                    ratio = longest_side*1./height
                    return (int(width*ratio), int(height*ratio))
            return (width, height)

        if self.type == 2:
            side = 500
        else:
            side = 1280

        (width, height) = image.size
        (width, height) = scale_dimensions(width, height, longest_side=side)

        size = (width, height)
        """ redimensiona esticando """
        # image = image.resize(size, Image.ANTIALIAS)
        """ redimensiona proporcionalmente """
        image.thumbnail(size, Image.ANTIALIAS)
        """ redimensiona cortando para encaixar no tamanho """
        # image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image.save(self.image.path, 'JPEG', quality=99)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = _(u'Banner')
        verbose_name_plural = _(u'Banners')


class Team(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('team', filename)

    name = models.CharField(_(u'Nome'), max_length=30)
    description = models.CharField(_(u'Descrição'), max_length=200)
    image = models.ImageField(_(u'Foto'), upload_to=get_file_path,
                              blank=True, null=True)

    def admin_image(self):
        if self.image.url:
            return '<img src="%s" width="60" />' % self.image.url
        else:
            return 'Sem imagem.'
    admin_image.allow_tags = True
    admin_image.short_description = 'Foto'

    def save(self, *args, **kwargs):
        if not self.id and not self.image:
            return

        super(Team, self).save(*args, **kwargs)

        image = Image.open(self.image)

        def scale_dimensions(width, height, longest_side):
            if width > height:
                if width > longest_side:
                    ratio = longest_side*1./width
                    return (int(width*ratio), int(height*ratio))
                elif height > longest_side:
                    ratio = longest_side*1./height
                    return (int(width*ratio), int(height*ratio))
            return (width, height)

        side = 400

        (width, height) = image.size
        (width, height) = scale_dimensions(width, height, longest_side=side)

        size = (width, height)
        """ redimensiona esticando """
        # image = image.resize(size, Image.ANTIALIAS)
        """ redimensiona proporcionalmente """
        # image.thumbnail(size, Image.ANTIALIAS)
        """ redimensiona cortando para encaixar no tamanho """
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image.save(self.image.path, 'JPEG', quality=99)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Equipe')
        verbose_name_plural = _(u'Equipe')
        ordering = ['name']


class Project(models.Model):
    title = models.CharField(_(u'Título'), max_length=200)
    body = tinymce_models.HTMLField(_(u'Conteúdo'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Projeto')
        verbose_name_plural = _(u'Projeto')
        ordering = ['title']


class Games(models.Model):
    title = models.CharField(_(u'Título'), max_length=200)
    body = tinymce_models.HTMLField(_(u'Conteúdo'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Jogo')
        verbose_name_plural = _(u'Jogos')
        ordering = ['title']
