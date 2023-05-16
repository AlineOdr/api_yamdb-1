import datetime as dt

from django.db import IntegrityError
from requests import request
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import (
    validate_bad_signs_in_username,
    validate_bad_value_in_username,
)


class RegisterDataSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей"""

    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_bad_signs_in_username,
            validate_bad_value_in_username,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        fields = ('username', 'email')
        model = User

    def create(self, validated_data):
        """Создание нового пользовательского объекта"""
        try:
            user = User.objects.get_or_create(**validated_data)[0]
        except IntegrityError:
            raise ValidationError('Такие User или Email уже есть')
        return user


class TokenSerializer(serializers.Serializer):
    """Серализатор для получения токена"""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для юзеров"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для своей учетной записи"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'pub_date')


import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    #rating = serializers.SerializerMethodField()

    # def get_rating(self, obj):
    #     rate = obj.reviews.aggregate(rating=Avg('score'))
    #     if not rate['rating']:
    #         return None
    #     return int(rate['rating'])

    def validate(self, attrs):
        year = attrs.get('year', 0)
        if year > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return attrs

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class TitleSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
        required=True,
        read_only=False,
        #queryset=Genre.objects.all()
    )
    category = CategorySerializer(
        required=True,
        read_only=False,
        #queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rate = obj.reviews.aggregate(rating=Avg('score'))
        if not rate['rating']:
            return None
        return int(rate['rating'])

    # def validate(self, attrs):
    #     year = attrs['year']
    #     if year > dt.datetime.now().year:
    #         raise serializers.ValidationError(
    #             'Нельзя добавлять произведения, которые еще не вышли!'
    #         )
    #     return attrs

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв дважды!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', 'pub_date')
