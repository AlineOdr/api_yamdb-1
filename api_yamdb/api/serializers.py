from reviews.models import Genre, User, Title, Comment, Review, Category
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

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
    #genre = GenreSerializer(read_only=False, many=True)
    #category = CategorySerializer(required=True)

    def validate(self, attrs):
        #year = self.context['request'].year
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
    
    
