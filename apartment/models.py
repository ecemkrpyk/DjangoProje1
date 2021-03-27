from django.db import models


#category tablosunu oluşturucaz, id eklemiyoruz otomatik ekler

class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),      #combobox
        ('False', 'Hayır'),

    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    #cascade ile ona bağlı şeylerde silinsin demek
    create_at = models.DateTimeField(auto_now_add=True)   #o andaki tarihi ekle
    update_at = models.DateTimeField(auto_now=True)    #her zamanki tarihi ekle

    def __str__(self):
        return self.title  #titleyi döndürür
