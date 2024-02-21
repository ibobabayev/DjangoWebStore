from django.contrib import admin
from catalog.models import Catalog,Product,Contact


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('pk','name')
    list_filter = ('name',)
    search_fields = ('name','description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk','name','price','category')
    list_filter = ('category',)
    search_fields = ('name','description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','number','email')
    list_filter = ('number',)
    search_fields = ('name','number')
