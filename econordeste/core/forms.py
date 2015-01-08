# coding: utf-8
from django import forms
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class ContactForm(forms.Form):
    name = forms.CharField(label=u'Nome',
                           widget=forms.TextInput(
                               attrs={'class': 'span12',
                                      'placeholder': 'Nome:'}))
    phone = forms.CharField(label=u'Fone',
                            widget=forms.TextInput(
                                attrs={'class': 'span12',
                                       'placeholder': 'Fone:'}))
    email = forms.EmailField(label=u'E-mail',
                             widget=forms.TextInput(
                                 attrs={'class': 'span12',
                                        'placeholder': 'E-mail:'}))
    subject = forms.CharField(label=u'Assunto',
                              widget=forms.TextInput(
                                  attrs={'class': 'span12',
                                         'placeholder': 'Assunto:'}))
    message = forms.CharField(label=u'Mensagem',
                              widget=forms.Textarea(
                                  attrs={'class': 'span12', 'rows': 6,
                                         'placeholder': 'Mensagem:'}))

    def send_mail(self):
        subject = u'Contato do site (%s)' % self.cleaned_data['name']
        context = {
            'name': self.cleaned_data['name'],
            'phone': self.cleaned_data['phone'],
            'email': self.cleaned_data['email'],
            'subject': self.cleaned_data['subject'],
            'message': self.cleaned_data['message'],
        }
        message = render_to_string('contact_mail.txt', context)
        message_html = render_to_string('contact_mail.html', context)
        msg = EmailMultiAlternatives(subject, message,
                                     'no-reply@econordeste.gov.br',
                                     ['contato@econordeste.gov.br'])

        msg.attach_alternative(message_html, 'text/html')
        msg.send()
