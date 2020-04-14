from django.db.models.functions import TruncDay
from django.db.models import Count
from django.contrib.auth.models import update_last_login

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer, PostSerializer, PostDetailSerializer,
    LikeSerializer, LikeAnalyticsSerializer, UserActivitySerializer
)
from .models import User, Post, Like


class UserCreationView(generics.CreateAPIView):
    '''
    For User registration
    '''
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostView(generics.ListCreateAPIView):
    '''
    Creats post and provide a list of all posts
    '''
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Provides information concerning particula post,
    aslo used for updating and deleteing of a particular post
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        return queryset


class LikesCounterView(generics.ListAPIView):
    '''
    to like and unlike a particular post by a particular user
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        user = self.request.user
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(id=post_id)

        if user in post.liked.all():
            post.liked.remove(user)
            Like.objects.filter(post_id=post_id, user=user).delete()
        else:
            post.liked.add(user)
            Like.objects.create(post_id=post_id, user=user)


class LikeAnalytics(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeAnalyticsSerializer

    def get_queryset(self):
        from_date = self.request.query_params.get('date_from')
        to_date = self.request.query_params.get('date_to')

        likes_per_day = (
            Like.objects
            .filter(like_date__gte=from_date, like_date__lte=to_date)
            .annotate(day=TruncDay('like_date'))
            .values('day')
            .annotate(likes=Count('id'))
        )
        return likes_per_day


class LastLogin(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = (
            User.objects.filter(id=user_id)
            .values('last_login', 'last_activity', 'username')
        )
        return queryset
