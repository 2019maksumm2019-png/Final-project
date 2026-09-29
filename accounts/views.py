from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy

from accounts.forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('recipe_list')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('recipe_list')


class RegisterView(CreateView):
    model = RegisterForm.Meta.model if hasattr(RegisterForm, 'Meta') else None
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')