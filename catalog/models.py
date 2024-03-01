from django.db import models

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
