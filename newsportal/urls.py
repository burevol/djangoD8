from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostCategoryView, upgrade_me, \
    subscribe, test_log

urlpatterns = [
    path('', cache_page(60)(PostList.as_view())),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/<int:pk>', cache_page(60*5)(PostCategoryView.as_view()), name='post_category'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('test_log', test_log, name='test_log'),
]
