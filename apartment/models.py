from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),      #combobox
        ('False', 'Hayır'),

    )
    title = models.CharField(blank=True,max_length=100)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    #cascade ile ona bağlı şeylerde silinsin demek
    create_at = models.DateTimeField(auto_now_add=True)   #o andaki tarihi ekle
    update_at = models.DateTimeField(auto_now=True)    #her zamanki tarihi ekle

    def __str__(self):
        return self.title  #titleyi döndürür

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'



class Apartment(models.Model):
    STATUS = (
        ('True', 'Evet'),      #combobox
        ('False', 'Hayır'),

    )
    #category tablosu ile bir ilişki kuruyoruz, category_id eklenmiş olur
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(blank=True,max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/') #klasör ismini değiştirebilirsin
    price=models.FloatField()
    amount=models.IntegerField()
    detail= RichTextUploadingField()
    slug = models.SlugField(max_length=150,blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)   #o andaki tarihi ekle
    update_at = models.DateTimeField(auto_now=True)    #her zamanki tarihi ekle

    def __str__(self):
        return self.title  #titleyi döndürür

    def image_tag(self): #image_tag eklenildiğinde hata veriyordu onun için böyle değiştirildi
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""

    image_tag.short_description = 'Image'


class Images(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    title= models.CharField(max_length=50, blank=True) #blank true boş geçmemize izin verir
    image= models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'












