from django.urls import path
from . import api_views

urlpatterns = [
    # CATEGORY
    path('categories/', api_views.category_list),
    path('categories/<int:pk>/', api_views.category_detail),
    path('categories/search/', api_views.category_search),
    path('categories/<int:pk>/topics/', api_views.category_topics),

    # TOPIC
    path('topics/', api_views.topic_list),
    path('topics/<int:pk>/', api_views.topic_detail),
    path('topics/search/', api_views.topic_search),

    # POST
    path('posts/', api_views.post_list),
    path('posts/<int:pk>/', api_views.post_detail),
    path('posts/search/', api_views.post_search),

    # USER POSTS
    path('users/posts/', api_views.user_posts),
]
