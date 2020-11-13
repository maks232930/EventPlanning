from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('events/', AllPostsListView.as_view(), name='all_posts'),
    path('event/<str:slug>/', view_news, name='post_detail'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
]
