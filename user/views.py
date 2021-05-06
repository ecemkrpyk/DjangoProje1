from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from apartment.models import Category, Comment, Apartment, ContentForm
from home.models import UserProfile

from user.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm


def index(request):
    category= Category.objects.all()
    current_user= request.user
    profile=UserProfile.objects.get(user_id=current_user.id)
   # return HttpResponse(profile)

    context={'category': category,
             'profile': profile,
            }
    return render(request, 'user_profile.html',context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user bizim user verimiz
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesap Güncellendi')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user) #user ile ilişki kursun
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) # OneToOneField ilişkisi user ile
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla güncellendi')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Lütfen aşağıdaki hatayı düzeltin.<br>' +str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category
    })

@login_required(login_url='/login')
def comments(request):
    category=Category.objects.all()
    current_user=request.user
    comments=Comment.objects.filter(user_id=current_user.id)

    context={'category': category,
             'comments': comments,
             }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request, 'Yorum silindi')
    return HttpResponseRedirect('/user/comments')





@login_required(login_url='/login')
def contents(request):
    category=Category.objects.all()
    current_user = request.user
    contents= Apartment.objects.filter(user_id=current_user.id) #userid yerine category id yazmıştın
    #mevcut user'ın contentleri çağırılır

    context = {'category': category,
               'contents': contents,
               }
    return render(request, 'user_contents.html', context)

@login_required(login_url='/login')
def addcontent(request):
    if request.method=='POST':
        form=ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data=Apartment()
            data.user_id=current_user.id

            data.title=form.cleaned_data['title']
            data.keywords=form.cleaned_data['keywords']
            data.description=form.cleaned_data['description']
            data.image=form.cleaned_data['image']
            data.category=form.cleaned_data['category']
            data.slug=form.cleaned_data['slug']
            data.detail=form.cleaned_data['detail']
            data.price = form.cleaned_data['price']
            data.amount = form.cleaned_data['amount']
            data.status='False'
            data.save()

            messages.success(request, 'Başarıyla eklendi')
            return  HttpResponseRedirect('/user/contents')
        else:
            messages.error(request,'İçerik eklenemedi')
            return HttpResponseRedirect('/user/addcontent') #hata vermişse add contente gidecek

    else:
        category = Category.objects.all()
        form=ContentForm()
        context= {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addcontent.html', context)



@login_required(login_url='/login')
def contentedit(request,id):
    content= Apartment.objects.get(id=id)
    if request.method=='POST':
        form=ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'içerik güncellendi')
            return  HttpResponseRedirect('/user/contents')
        else:
            messages.error(request, 'içerik güncellenemedi')
            return HttpResponseRedirect('/user/contentedit')
    else:
        category=Category.objects.all()
        form = ContentForm(instance=content) #İÇERİĞİ DOLDURUYORUZ, FORM DOLU GELİR
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def contentdelete(request,id):
    current_user = request.user
    Apartment.objects.filter(id=id, user_id=current_user.id). delete()
    messages.success(request, 'içerik silindi')
    return  HttpResponseRedirect('/user/contents')





























