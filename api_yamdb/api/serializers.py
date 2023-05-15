import datetime as dt

from django.db import IntegrityError
from rest_framework import serializers
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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    # genre = GenreSerializer(read_only=False, many=True)
    # category = CategorySerializer(required=True)

    def validate(self, attrs):
        # year = self.context['request'].year
        year = attrs['year']
        if year > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return attrs

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', 'author', 'pub_date')
