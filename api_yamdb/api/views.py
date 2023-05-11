from django.shortcuts import get_object_or_404
#from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Genre, User, Title, Comment, Review, Category
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

#from .permissions import OwnerOnly, OwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
)


class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        serializer.save(rating=0)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
