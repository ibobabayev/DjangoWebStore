from django.shortcuts import render
from catalog.models import Product,Contact , Blogpost
from django.views.generic import ListView,DetailView,TemplateView , CreateView , DeleteView , UpdateView
from django.urls import reverse_lazy , reverse
from pytils.translit import slugify
from django.core.mail import send_mail


# def home(request):
#     products = Product.objects.all()
#     product_list = {'products_list': products}
#     return render(request,'product_list.html',product_list)

class ProductListView(ListView):
    model = Product
    extra_context = {'products_list': Product.objects.all()}

# def latest_list.html(request):
#     product_list = Product.objects.order_by('price')[:5]
#     products = {'filtred_list': product_list}
#     return render(request, 'latest_list.html', products)



class LatestListView(ListView):
    model = Product
    template_name = 'catalog/latest_list.html'
    product_list = Product.objects.order_by('price')[:5]
    extra_context = {'filtred_list': product_list}


# def contact(request):
#     contact_info = Contact.objects.all()
#     contact_info = {'contact_book':contact_info}
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'Имя:{name} , номер телефона:{phone} , сообщение: {message}')
#     return render(request,'contact.html',contact_info)

class ContactTemplateView(TemplateView):
    template_name = 'catalog/contact.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        contact_info = Contact.objects.all()
        context_data['contact_book'] = contact_info
        return context_data

    def post(self,request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя:{name} , номер телефона:{phone} , сообщение: {message}')
        return render(request,self.template_name)


# def products(request,pk):
#     product = Product.objects.filter(id=pk)
#     product_list = {'products_list' : product}
#     return render(request,'product_detail.html',product_list)

class ProductDetailView(DetailView):
    model = Product


class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = ('name','description','preview',)
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        if form.is_valid:
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()

        return super().form_valid(form)

class BlogpostUpdateView(UpdateView):
    model = Blogpost
    fields = ('name','description','preview',)

    def get_success_url(self):
        return reverse('catalog:view',args=[self.kwargs.get('pk')])

class BlogpostListView(ListView):
    model = Blogpost

    def get_queryset(self,*args,**kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

class BlogpostDetailView(DetailView):
    model = Blogpost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count = int(self.object.views_count) + 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail(
                'Поздравляем с достижением!',
                'Опубликованная вами статья достигла отметки в 100 просмотром!',
                'me@mail.com','you@mail.com',
                fail_silently=False,
            )

        return self.object


class BlogpostDeleteView(DeleteView):
    model = Blogpost
    success_url = reverse_lazy('catalog:list')