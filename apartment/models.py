from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models


from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),      #combobox
        ('False', 'Hayır'),

    )
    title = models.CharField(blank=True,max_length=100)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    #cascade ile ona bağlı şeylerde silinsin demek
    create_at = models.DateTimeField(auto_now_add=True)   #o andaki tarihi ekle
    update_at = models.DateTimeField(auto_now=True)    #her zamanki tarihi ekle

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self): #alt kategorileride göstermesi için
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})



class Apartment(models.Model):
    STATUS = (
        ('True', 'Evet'),      #combobox
        ('False', 'Hayır'),

    )

    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #category tablosu ile bir ilişki kuruyoruz, category_id eklenmiş olur
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(blank=True,max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/') #klasör ismini değiştirebilirsin
    price=models.FloatField()
    amount=models.IntegerField(blank=True)
    detail= RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
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

    def get_absolute_url(self): #otomatik slug oluşturur
        return reverse('apartment_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    title= models.CharField(max_length=50, blank=True) #blank true boş geçmemize izin verir
    image= models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ContentImageForm(ModelForm): #validation için
    class Meta:
        model=Images
        fields=['title', 'image']


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),  # combobox
        ('False', 'Hayır'),

    )
    apartment=models.ForeignKey(Apartment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject', 'comment', 'rate']


#user bir içerik ekleyeceği zaman
class ContentForm(ModelForm):

    class Meta:
        model = Apartment #form apartmenta bağlı
        fields = ('category','title', 'keywords', 'description', 'image', 'detail', 'slug','price','amount')
        widgets = {
            'title'     : TextInput(attrs={'class': 'form-control mb-30','placeholder':'title'}),
            'slug'   : TextInput(attrs={'class': 'form-control mb-30','placeholder':'slug'}),
            'keywords': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'keywords'}),
            'price': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'price'}), #textınputu düzelt sonra
            'description': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'description'}),
            'amount': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'amount'}),
            'category'      : Select(attrs={'class': 'form-control mb-30','placeholder':'category'} ),
            'image'     : FileInput(attrs={'class': 'form-control mb-30', 'placeholder': 'image', }),
            'detail': CKEditorWidget(), #ckeditor input
        }













