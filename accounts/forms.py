from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Введите Ваш email')
    first_name = forms.CharField(label='Введите Ваше имя')
    last_name = forms.CharField(label='Введите Вашу фамилию')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',

        )


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name='common users')
        user.groups.add(common_users)
        return user
