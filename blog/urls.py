from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('events/', views.AllPostsListView.as_view(), name='all_posts'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('event/<str:slug>/', views.view_news, name='post_detail'),
    path('category/<str:slug>/', views.PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', views.PostsByTag.as_view(), name='tag'),
    path('search/', views.Search.as_view(), name='search'),
]
