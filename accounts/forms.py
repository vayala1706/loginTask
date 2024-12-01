from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
    )
    age = forms.IntegerField(
        label=_("Age"),
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "age", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered.'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.age = self.cleaned_data.get("age")
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
    )
    age = forms.IntegerField(
        label=_("Age"),
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "age"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered.'))
        return email