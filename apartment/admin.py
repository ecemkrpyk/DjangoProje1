from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from apartment.models import Category, Apartment, Images


class ApartmentImageInline(admin.TabularInline):
    model = Images   #ımages tablosundan
    extra = 5   #galeri extra kaç resimden oluştuğu

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status'] #statuse göre filtreleme

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Apartment,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Apartment,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [ApartmentImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'apartment', 'image_tag']
    readonly_fields = ('image_tag',)



admin.site.register(Category, CategoryAdmin2)  #categorynin adminde gözükmesini sağlar
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Images, ImagesAdmin)












