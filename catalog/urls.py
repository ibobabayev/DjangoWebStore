from django.urls import path
from catalog.views import home,contact,latest

urlpatterns = [
    path('', home),
    path('contact/', contact),
    path('latest/', latest)
]