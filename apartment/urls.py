from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'), #home da herhangi bir şey girilmezse indexi kullan demek
    path('addcomment/<int:id>', views.addcomment, name='addcomment')















]