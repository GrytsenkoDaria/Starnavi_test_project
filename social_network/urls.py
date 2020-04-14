from django.urls import path

from rest_framework.authtoken import views

from .views import UserCreationView, PostView, PostDetailView
from .views import LikesCounterView, LikeAnalytics
from .views import LastLogin

urlpatterns = [
    path('registration/', UserCreationView.as_view()),
    path('login/', views.obtain_auth_token),
    path('posts/', PostView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:post_pk>/like', LikesCounterView.as_view()),
    path('analytics/', LikeAnalytics.as_view()),
    path('activity/', LastLogin.as_view()),
]
