from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from news.models import Author
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import SignupForm, CustomSignUpForm
from allauth.account.views import LoginView, LogoutView


# class LogIn(LoginView):
#     form_class = CustomLogInForm
#     template_name = 'account/login.html'
#     success_url = '/news'


class SignUp(CreateView):
    model = User
    form_class = CustomSignUpForm
    success_url = '/accounts/login'
    template_name = 'account/signup.html'

    def post(self, request, *args, **kwargs):
        info = User(username=request.POST['username'])
        info.save()

        send_mail(
            subject=info.username,
            message='Test message',
            from_email='yuran4ek37@yandex.ru',
            recipient_list=[],
        )
        return redirect(request.META.get('HTTP_REFERER'))

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
