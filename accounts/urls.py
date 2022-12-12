from django.urls import path, include
from .views import SignUp, LogOut, update_user_group


urlpatterns = [
    path('', include('allauth.urls')),
    path('signup/', SignUp.as_view(), name='accounts_signup'),
    path('logout/', LogOut.as_view(), name='accounts_logout'),
    path('', update_user_group, name='become_author'),

]
