from django.contrib import admin

# Register your models here.
from apartment.models import Category, Apartment, Images

class ApartmentImageInline(admin.TabularInline):
    model = Images   #ımages tablosundan
    extra = 5   #galeri extra kaç resimden oluştuğu

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status'] #statuse göre filtreleme

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [ApartmentImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'apartment', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category, CategoryAdmin)  #categorynin adminde gözükmesini sağlar
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Images, ImagesAdmin)











