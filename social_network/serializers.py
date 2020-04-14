from rest_framework import serializers

from social_network.models import User, Post, Like


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, email):
        email_exist = (
            User.objects.filter(email=email).exists()
        )
        if email_exist:
            raise serializers.ValidationError(
                'Such email is already used. Please, try another one'
            )

        return email


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'num_likes', 'author']
        extra_kwargs = {
            'num_likes': {'read_only': True},
            'author': {'read_only': True},
        }

    def create(self, validated_data):
        author_id = self.context['request'].user.pk
        validated_data['author_id'] = author_id
        post = super().create(validated_data)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer
    post = PostSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class LikeAnalyticsSerializer(serializers.Serializer):
    likes = serializers.IntegerField()
    day = serializers.DateTimeField()


class UserActivitySerializer(serializers.Serializer):
    last_login = serializers.DateTimeField()
    username = serializers.CharField()
    last_activity = serializers.DateTimeField()
