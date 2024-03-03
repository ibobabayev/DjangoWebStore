from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home,contact,latest,products

app_name = CatalogConfig.name


urlpatterns = [
    path('', home),
    path('contact/', contact,name='contact'),
    path('latest/', latest,name='latest'),
    path('<int:pk>/products/', products,name='products'),
]