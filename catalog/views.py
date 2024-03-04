from django.shortcuts import render
from catalog.models import Product,Contact,Catalog

# Create your views here.
def home(request):
    products = Product.objects.all()
    product_list = {'products_list': products}
    return render(request,'home.html',product_list)

def latest(request):
    product_list = Product.objects.order_by('price')[:5]
    products = {'filtred_list': product_list}
    return render(request, 'latest.html', products)

def contact(request):
    contact_info = Contact.objects.all()
    contact_info = {'contact_book':contact_info}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя:{name} , номер телефона:{phone} , сообщение: {message}')
    return render(request,'contact.html',contact_info)

def products(request,pk):
    product = Product.objects.get(pk=pk)
    product_list = {'products_list' : product}
    return render(request,'products.html',product_list)
