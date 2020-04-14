from django.urls import path

from .views import UserCreationView, PostView, PostDetailView
from .views import LikesCounterView, LikeAnalytics
from .views import LoginToken, LastLogin

urlpatterns = [
    path('registration/', UserCreationView.as_view()),
    path('login/', LoginToken.as_view()),

    path('posts/', PostView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:post_pk>/like', LikesCounterView.as_view()),
    path('analytics/', LikeAnalytics.as_view()),
    path('activity/', LastLogin.as_view()),
]
