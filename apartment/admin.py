from django.contrib import admin

# Register your models here.
from apartment.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status'] #statuse göre filtreleme

admin.site.register(Category,CategoryAdmin) #categorynin adminde gözükmesini sağlar