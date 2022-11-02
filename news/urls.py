from django.urls import path
from .views import PostList, PostDetail


urlpatterns = [
    path('', PostList.as_view()),
    path('oneNews/<int:pk>', PostDetail.as_view()),
]
