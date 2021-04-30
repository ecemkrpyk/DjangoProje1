from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from apartment.models import CommentForm, Comment


def index(request):
    return HttpResponse("Apartment Page")


@login_required(login_url='/login') #eğer login edilmediyse buraya izin vermez
def addcomment(request, id):
   url = request.META.get('HTTP_REFERER')  # en son olduğumuz url e dönmemiz için
   if request.method == 'POST': #form post edildiyse
      form = CommentForm(request.POST)
      if form.is_valid():
         current_user=request.user #login olan userdan getirilir

         data = Comment()  #model ile bağlantı kur
         data.user_id= current_user.id
         data.apartment_id= id
         data.subject = form.cleaned_data['subject'] #bu 3 eleman geldiyse form valid dir
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']

         data.ip = request.META.get('REMOTE_ADDR') #bilgisayarın ip'si
         data.save()  # veritabanına kaydet
         messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz")

         return HttpResponseRedirect(url)

   messages.warning(request, "Yorumunuz kaydedilmedi.Lütfen kontrol ediniz")
   return HttpResponseRedirect(url)

































