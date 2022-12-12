from django import forms
from django.shortcuts import redirect

from news.models import Author
from django.contrib.auth.models import User, Group
from django.utils.functional import lazy
from django.utils.translation import gettext, gettext_lazy as _, pgettext

from allauth.account.forms import SignupForm

gettext_lazy = lazy(gettext, str)
pgettext_lazy = lazy(pgettext, str)


class CustomSignUpForm(SignupForm):

    first_name = forms.CharField(label='Ваше имя',
                                 widget=forms.TextInput(
                                     attrs={"placeholder": _("Введите Ваше имя"), "autocomplete": "имя"}
                                 ))
    last_name = forms.CharField(label='Ваша фамилия',
                                widget=forms.TextInput(
                                    attrs={"placeholder": ("Введите Вашу фамилию"), "autocomplete": "фамилия"}
                                ))

    def save(self, request):
        user = super().save(request)
        # user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        common_users = Group.objects.get(name='common users')
        user.groups.add(common_users)
        return user


