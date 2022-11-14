from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = 'timeIn'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_in'] = Post.objects.get(timeIn)


class PostSearch(ListView):
    model = Post
    ordering = 'timeIn'
    template_name = 'newsSearch.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'oneNews.html'
    context_object_name = 'oneNews'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'newsCreate.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'newsUpdate.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'newsDelete.html'
    success_url = reverse_lazy('news_list')
