from django.shortcuts import render
from catalog.models import Product,Contact

# Create your views here.
def home(request):
    print(Product.objects.order_by('price')[:5])
    return render(request,'home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя пользователя: {name}, email: {email} , номер: {phone} , Отзыв: {message}')
    return render(request,'contact.html',{'contact_book':Contact.objects.all()})