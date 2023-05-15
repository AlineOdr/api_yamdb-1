from django.shortcuts import get_object_or_404
from .serializers import TokenSerializer
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
    RegisterDataSerializer,
    UserSerializer
)

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrModeratorOrAuthorOrReadOnly
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.forms import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Функция для регистрации новых пользователей"""

    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDB registration',
        message=f'Confirmation code: {confirmation_code}',
        from_email=settings.TOKEN_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
    return Response(
        {'confirmation_code': ['неверный код подтверждения']},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


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

