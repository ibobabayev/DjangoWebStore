from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from users.forms import UserRegisterForm , UserProfileForm
from users.models import User
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy , reverse
import random

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Поздравляем с успешной регистрацией на нашем магазине!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        return self.request.user

def reset_password(request):
    new_password = ''.join([str(random.randint(0,9)) for _ in range(8)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль : {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))