import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.db.models.signals import m2m_changed
from django.views.generic import ListView, UpdateView, CreateView, DetailView, \
    DeleteView
from django.core.cache import cache
from django.http import HttpResponse

from .forms import NewsForm
from .models import Post, Category
from .tasks import send_new_article_mail


# Create your views here.
class PostCategoryView(ListView):
    model = Post
    template_name = 'posts_category.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self):
        id = self.kwargs.get('pk')
        return Post.objects.filter(postcategory__category_id=id)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=id).name
        context['category_id'] = id
        context['is_subscribed'] = Category.objects.get(pk=id).subscribers.exists()
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)

        return obj


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    template_name = 'post_create.html'
    form_class = NewsForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post')
    template_name = 'post_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearchView(ListView):
    model = Post
    template_name = 'posts_search.html'


@login_required()
def upgrade_me(request):
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(request.user)
    return redirect('/news/')


@login_required()
def subscribe(request, pk):
    if not Category.objects.get(pk=pk).subscribers.filter(id=request.user.id).exists():
        cat = Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


def article_added(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_new_article_mail.delay(instance.id)


def test_log(request):
    logger_django = logging.getLogger('django')
    logger_django_request = logging.getLogger('django.request')
    logger_django_server = logging.getLogger('django.server')
    logger_django_template = logging.getLogger('django.template')
    logger_django_db_backends = logging.getLogger('django.db_backends')
    logger_django_security = logging.getLogger('django.security')

    logger_django.debug("django debug message")
    logger_django.info('django info message')
    logger_django.warning('django warning message')
    logger_django.error('django error message')
    logger_django.critical('django critical message')

    logger_django_request.debug("logger_django_request debug message")
    logger_django_request.info('logger_django_request info message')
    logger_django_request.warning('logger_django_request warning message')
    logger_django_request.error('logger_django_request error message')
    logger_django_request.critical('logger_django_request critical message')

    logger_django_server.debug("logger_django_server debug message")
    logger_django_server.info('logger_django_server info message')
    logger_django_server.warning('logger_django_server warning message')
    logger_django_server.error('logger_django_server error message')
    logger_django_server.critical('logger_django_server critical message')

    logger_django_template.debug("logger_django_template debug message")
    logger_django_template.info('logger_django_template info message')
    logger_django_template.warning('logger_django_template warning message')
    logger_django_template.error('logger_django_template error message')
    logger_django_template.critical('logger_django_template critical message')

    logger_django_db_backends.debug("logger_django_db_backends debug message")
    logger_django_db_backends.info('logger_django_db_backends info message')
    logger_django_db_backends.warning('logger_django_db_backends warning message')
    logger_django_db_backends.error('logger_django_db_backends error message')
    logger_django_db_backends.critical('logger_django_db_backends critical message')

    logger_django_security.debug("logger_django_security debug message")
    logger_django_security.info('logger_django_security info message')
    logger_django_security.warning('logger_django_security warning message')
    logger_django_security.error('logger_django_security error message')
    logger_django_security.critical('logger_django_security critical message')

    return HttpResponse(status=200)

m2m_changed.connect(article_added, sender=Post.category.through)
