from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.core.cache import cache

from news.custom_mixins import OwnerPermissionRequiredMixin

from NewsPortal import settings
from .models import Post, Comment, Author, Category, SubscribeCategories
from .filters import PostFilter
from .forms import PostForm, CommentForm
from datetime import datetime, timedelta


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
    ordering = '-timeIn'
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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


def delete_comment(request, **kwargs):
    selected_comments = Comment.objects.get(pk=int(kwargs['pk']))
    selected_comments.delete()
    return redirect(request.META.get('HTTP_REFERER'))


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'newsCreate.html'

    def form_valid(self, form):
        form.instance.postAuthor = self.request.user.author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        limits: int = settings.DAILY_POST_LIMIT
        prev_day = datetime.now() - timedelta(days=1)
        posts_day_count: list = Post.objects.filter(postAuthor__users=self.request.user,
                                                    timeIn__gte=prev_day)
        context['post_limits'] = limits > len(posts_day_count)
        return context


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


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategories=self.postCategories).order_by('-timeIn')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategories.subscribers.all()
        context['category'] = self.postCategories
        return context


def subscribe_unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    sample_html = ''
    if user not in category.subscribers.all():
        category.subscribers.add(user)
        sample_html = 'account/email/email_subscribe_information.html'
    elif user in category.subscribers.all():
        category.subscribers.remove(user)
        sample_html = 'account/email/email_unsubscribe_information.html'

    html_content = render_to_string(
        sample_html,
        {
            'new_user': user.username,
            'link': f'{settings.SITE_URL}/news/',
            'categories': category,
            'category_link': f'{settings.SITE_URL}/news/categories/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Информация о подписке',
        body='',
        from_email='yuran4ek37@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    return redirect(request.META.get('HTTP_REFERER'))
    # return render(request, s_html, {'category': category})
