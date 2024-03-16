from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView,ContactTemplateView,LatestListView,ProductDetailView , BlogpostCreateView, BlogpostListView , BlogpostDetailView,BlogpostUpdateView, BlogpostDeleteView , ProductCreateView, ProductUpdateView,ProductDeleteView

app_name = CatalogConfig.name


urlpatterns = [
    path('', ProductListView.as_view(),name='home'),
    path('contact/', ContactTemplateView.as_view(),name='contact'),
    path('latest_list/', LatestListView.as_view(),name='latest'),
    path('products/<int:pk>', ProductDetailView.as_view(),name='products'),
    path('create/', BlogpostCreateView.as_view(),name='create_blog'),
    path('list/', BlogpostListView.as_view(),name='list'),
    path('view/<int:pk>', BlogpostDetailView.as_view(),name='view'),
    path('edit/<int:pk>', BlogpostUpdateView.as_view(),name='edit'),
    path('delete/<int:pk>', BlogpostDeleteView.as_view(),name='delete'),
    path('create_product/', ProductCreateView.as_view(),name='create_product'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(),name='update_product'),
    path('delete_product/<int:pk>', ProductDeleteView.as_view(),name='delete_product'),
]
