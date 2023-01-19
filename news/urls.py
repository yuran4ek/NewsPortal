from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, delete_comment, \
    CategoryListView, subscribe_unsubscribe


urlpatterns = [
    path('', PostList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('<int:pk>/del/', delete_comment, name='delete_comment'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe_unsubscribe, name='subscribe_unsubscribe'),

]
