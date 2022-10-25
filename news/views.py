from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'timeIn'
    template_name = 'news.html'
    context_object_name = 'news'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_in'] = Post.objects.get(timeIn)

class PostDetail(DetailView):
    model = Post
    template_name = 'oneNews.html'
    context_object_name = 'oneNews'
