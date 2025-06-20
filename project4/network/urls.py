
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('addPost', views.addPost, name='addPost'),
    path('getPosts', views.getPosts, name='getPosts'),
    path('user/<int:pk>/page', views.userpage, name='userpage'),
    path('getPosts/<int:pk>', views.getuserPostList, name='getUserPosts'),
    path('follow', views.follow, name='follow'),
    path('following', views.following, name='following'),
    path('post/<int:pk>/like', views.likePost, name='likePost'),
    path('post/<int:pk>/delete', views.deletePost, name='deletePost'),
    path('post/<int:pk>/edit', views.editPost ,name='editPost')
]
