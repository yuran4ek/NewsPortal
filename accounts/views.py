from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView

from news.models import Author
from .forms import CustomSignUpForm
from allauth.account.views import LogoutView


# class LogIn(LoginView):
#     form_class = CustomLogInForm
#     template_name = 'account/login.html'
#     success_url = '/news'


class SignUp(CreateView):
    model = User
    form_class = CustomSignUpForm
    success_url = '/accounts/login'
    template_name = 'account/signup.html'


class LogOut(LogoutView):
    template_name = 'accounts/logout.html'


def update_user_group(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(users=User.objects.get(pk=user.id))

    return render(request, 'become_author.html')
