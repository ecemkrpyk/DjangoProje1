from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage
from django.contrib import messages


def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page' : 'home'}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarımız.html', context)

def iletisim(request):

    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR') #clientın ip'sini alma
            data.save() #veritabanına kaydet

            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz") #flash mesaj
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form': form}
    return render(request, 'iletisim.html', context)