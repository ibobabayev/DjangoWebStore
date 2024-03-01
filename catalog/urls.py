from django.urls import path
from catalog.views import home,contact,latest,products

urlpatterns = [
    path('', home),
    path('contact/', contact),
    path('latest/', latest),
    path('products/', products),
]