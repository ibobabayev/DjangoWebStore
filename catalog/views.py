from django.shortcuts import render
from catalog.models import Product,Contact

# Create your views here.
def home(request):
    return render(request,'home.html')

def latest(request):
    product_list = Product.objects.order_by('price')[:5]
    products = {'filtred_list': product_list}
    return render(request, 'latest.html', products)
# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'Имя пользователя: {name}, email: {email} , номер: {phone} , Отзыв: {message}')
#     return render(request,'contact.html',{'contact_book':Contact.objects.all()})
def contact(request):
    contact_info = Contact.objects.all()
    contact_info = {'contact_book':contact_info}
    return render(request,'contact.html',contact_info)