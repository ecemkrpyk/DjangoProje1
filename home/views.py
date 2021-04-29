from unicodedata import category

from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from apartment.models import Apartment, Category
from home.models import Setting, ContactForm, ContactFormMessage
from django.contrib import messages


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata= Apartment.objects.all()[:4] #4 tane veri getirir
    category= Category.objects.all()
    dayapartments=Apartment.objects.all()[:4]
    lastapartments = Apartment.objects.all().order_by('-id')[:4]
    randomapartments = Apartment.objects.all().order_by('?')[:4]



    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayapartments': dayapartments,
               'lastapartments': lastapartments,
               'randomapartments': randomapartments
               }
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


def category_apartments(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    apartments=Apartment.objects.filter(category_id=id)

    context= {'apartments': apartments,
              'category': category,
              'categorydata': categorydata
             }
    return render (request, 'apartments.html', context)