from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from catalog.models import Product, Contact, Blogpost, Version, Catalog
from django.views.generic import ListView,DetailView,TemplateView , CreateView , DeleteView , UpdateView
from django.urls import reverse_lazy , reverse
from pytils.translit import slugify
from django.core.mail import send_mail
from catalog.forms import ProductForm, VersionForm
from django.forms import inlineformset_factory

from catalog.services import cached_categories, cached_products


# def home(request):
#     products = Product.objects.all()
#     product_list = {'products_list': products}
#     return render(request,'product_list.html',product_list)
class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    login_url = "users:login"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if form.is_valid:
            new_product = form.save()
            new_product.slug = slugify(new_product.name)
            new_product.save()
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    login_url = "users:login"
    # permission_required = ('catalog.set_published', 'catalog.change_description','catalog.change_category')

    def get_success_url(self):
        return reverse('catalog:products', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product,Version,form=VersionForm,extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        version_form = context_data['formset']
        self.object = form.save()
        if version_form.is_valid():
            version_form.instance = self.object
            version_form.save()
        return super().form_valid(form)
class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    login_url = "users:login"

class ProductListView(ListView):
    model = Product
    # extra_context = {'products_list': Product.objects.all()}

    def get_queryset(self,*args,**kwargs):
        queryset = super().get_queryset(*args,**kwargs)
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args,**kwargs)
        # context_data['products_list'] = Product.objects.all()
        context_data['products_list'] = cached_products()
        return context_data


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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product = self.get_object()
        context_data['versions'] = Version.objects.filter(product=product)
        context_data['current_version'] = Version.objects.filter(product=product).filter(is_active=True).first()
        return context_data

class BlogpostCreateView(LoginRequiredMixin,CreateView):
    model = Blogpost
    fields = ('name','description','preview',)
    success_url = reverse_lazy('catalog:list')
    login_url = "users:login"

    def form_valid(self, form):
        if form.is_valid:
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()

        return super().form_valid(form)

class BlogpostUpdateView(LoginRequiredMixin,UpdateView):
    model = Blogpost
    fields = ('name','description','preview',)
    login_url = "users:login"


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
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail(
                'Поздравляем с достижением!',
                'Опубликованная вами статья достигла отметки в 100 просмотром!',
                'me@mail.com','you@mail.com',
                fail_silently=False,
            )

        return self.object


class BlogpostDeleteView(LoginRequiredMixin,DeleteView):
    model = Blogpost
    success_url = reverse_lazy('catalog:list')
    login_url = "users:login"


class CatalogListView(ListView):
    model = Catalog
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['categories_list'] = cached_categories()
        return context_data
