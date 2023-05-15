from requests import request
from reviews.models import Genre, Title, Category, User, Comment, Review
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt
from django.shortcuts import get_object_or_404
from django.db.models import Avg

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
        
    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get("view").kwargs.get("title_id")
        title =  get_object_or_404(Title, pk=title_id)
        if self.context.get('request').method == 'POST':
            if  Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                'Нельзя оставить отзыв дважды!')
        return data

    


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', 'pub_date')
