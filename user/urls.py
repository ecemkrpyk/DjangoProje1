from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'), #home da herhangi bir şey girilmezse indexi kullan demek
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
]