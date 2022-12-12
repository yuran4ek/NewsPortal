from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import FormMixin

from news.custom_mixins import OwnerPermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Author
from .filters import PostFilter
from .forms import PostForm, CommentForm


class PostList(ListView):
    model = Post
    ordering = '-timeIn'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    ordering = 'timeIn'
    template_name = 'newsSearch.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView, FormMixin):
    model = Post
    form_class = CommentForm
    template_name = 'oneNews.html'
    context_object_name = 'oneNews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_now'] = self.request.user
        context['commnts'] = Comment.objects.filter(postComment=self.kwargs.get("pk"))
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.form = form.save(commit=False)
        self.form.postComment = Post.objects.get(pk=self.kwargs.get("pk"))
        self.form.userComment = self.request.user
        form.save()
        return super(PostDetail, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('news_detail', kwargs={'pk': self.kwargs.get('pk')})


def delete_comment(request, **kwargs):
    selected_comments = Comment.objects.get(pk=int(kwargs['pk']))
    selected_comments.delete()

    return redirect(request.META.get('HTTP_REFERER'))


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'newsCreate.html'


class PostUpdate(OwnerPermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'newsUpdate.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postAuthor = Author.objects.get(users=self.request.user)
        return super().form_valid(form)


class PostDelete(OwnerPermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'newsDelete.html'
    success_url = reverse_lazy('news_list')
