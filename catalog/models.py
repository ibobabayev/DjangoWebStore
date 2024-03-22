from django.db import models
from django.conf import settings

class Catalog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}({self.description})'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='product/',null=True,blank=True,verbose_name='Изображение')
    category = models.ForeignKey(Catalog,on_delete = models.CASCADE)
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(null=True,blank=True,verbose_name='Дата создания')
    updated_at = models.DateField(null=True,blank=True,verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,verbose_name='Владелец',on_delete=models.SET_NULL)
    #manufactured_at = models.DateField(null=True,blank=True,verbose_name='Дата производства продукта')
    def __str__(self):
        return f'Имя продукта: {self.name}  Категория:{self.category}   Цена: {self.price} рублей'

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Contact(models.Model):
    name = models.CharField(max_length=50,verbose_name='Имя')
    number = models.TextField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return f'{self.name} {self.number}'

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Blogpost(models.Model):
    name = models.CharField(max_length=50,verbose_name="Имя")
    slug = models.CharField(max_length=50,verbose_name="slug")
    description = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='product/',null=True,blank=True,verbose_name='Изображение')
    created_at = models.DateField(null=True,blank=True,verbose_name='Дата создания')
    is_published = models.BooleanField(default=True,verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0,verbose_name='Просмотры')

    def __str__(self):
        return f"{self.name}, {self.description}, {self.created_at}"

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class Version(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Наименование')
    version_number = models.IntegerField(verbose_name="номер версии")
    version_name = models.CharField(max_length=100,verbose_name="название версии")
    is_active = models.BooleanField(default=True,verbose_name='активная версия')

    def __str__(self):
        return f"{self.product}, {self.version_number}, {self.version_name}"

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
