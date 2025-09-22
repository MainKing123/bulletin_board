from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    ResponseListView, accept_response, reject_response, response_toggle_view,
    MyPostListView, register_view, confirm_email_view, profile_view
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('myposts/', MyPostListView.as_view(), name='my_post_list'),
    path('', views.ad_list, name='ad_list'),

    path('responses/', ResponseListView.as_view(), name='response_list'),
    path('responses/<int:pk>/accept/', accept_response, name='accept_response'),
    path('responses/<int:pk>/reject/', reject_response, name='reject_response'),
    path('responses/<int:pk>/toggle/', response_toggle_view, name='response_toggle'),
    path('post/<int:pk>/response/', views.response_create, name='response_create'),
    path('register/', register_view, name='register'),
    path('confirm/', confirm_email_view, name='confirm_email'),
    path('account/', profile_view, name='account'),
    path('profile/', views.profile_view, name='profile'),

]
