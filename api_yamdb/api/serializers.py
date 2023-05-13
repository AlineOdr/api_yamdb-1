from reviews.models import Genre, Title, Category, User, Comment, Review
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=True,
        read_only=False,
        slug_field='name',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        required=True,
        read_only=False,
        slug_field='name',
        queryset=Category.objects.all()
    )

    def validate(self, attrs):
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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        validators = (validators.UniqueTogetherValidator(
                      queryset=Review.objects.all(),
                      fields=('title', 'author',),
                      message='Нельзя оставить отзыв дважды!'
                      ),)

    def validate(self, value):
        if not 0 > value > 11:
            raise serializers.ValidationError(
                'Оцените от 0 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'pub_date')
