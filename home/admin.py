from django.contrib import admin

# Register your models here.

from home.models import Setting, ContactFormMessage, UserProfile

admin.site.register(Setting)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message','note', 'status']
    list_filter=['status']

admin.site.register(ContactFormMessage,ContactFormMessageAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','address','city', 'country', 'image_tag']


admin.site.register(UserProfile,UserProfileAdmin)















