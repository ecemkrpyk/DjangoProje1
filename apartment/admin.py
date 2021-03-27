from django.contrib import admin

# Register your models here.
from apartment.models import Category, Apartment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status'] #statuse göre filtreleme

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount', 'status']
    list_filter = ['status','category']

admin.site.register(Category,CategoryAdmin) #categorynin adminde gözükmesini sağlar
admin.site.register(Apartment,ApartmentAdmin)