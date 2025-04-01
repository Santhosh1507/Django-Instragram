from django.contrib import admin
from django.urls import path
from my_instra import settings
from authuser import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('loginn/',views.loginn),
    path('signup/',views.signup),
    path('logoutt/',views.logoutt),
    path('upload',views.upload),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
    path('comment-post/<str:post_id>', views.comment_post, name='comment_post'),
    path('follower', views.follower, name='follow'),
    path('notifications', views.notifications, name='notifications'),
    path("check-notifications/", views.check_notifications, name="check_notifications"),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    
]
