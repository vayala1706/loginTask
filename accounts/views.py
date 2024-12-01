from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView)  # Añadido
from django.contrib.auth.mixins import UserPassesTestMixin  # Añadido
from .forms import CustomUserCreationForm, UserUpdateForm

User = get_user_model()

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm  # Using your custom form
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tasks:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_pw)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Account created successfully for {username}!')
        return response
    
class UserDetail(DetailView, OnlyYouMixin):
    model = User
    template_name = 'accounts/user_detail.html'
# Aquí termina

class UserUpdate(UpdateView, OnlyYouMixin):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})

class UserDelete(DeleteView, OnlyYouMixin):
    model = User
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'
    