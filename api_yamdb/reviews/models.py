from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework import status

from api.validators import validate_bad_value_in_username
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'администратор'),
        (MODERATOR, 'модератор'),
        (USER, 'пользователь'),
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='allows 150 characters or fewer @/./+/-/_ and digits',
                code=status.HTTP_400_BAD_REQUEST,
            ),
            validate_bad_value_in_username,
        ],
    )
    email = models.EmailField(max_length=254, unique=True, blank=False)
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль',
        max_length=max(map(len, [role for role, _ in ROLE_CHOICES])),
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[
                                RegexValidator(
                                    regex='^[-a-zA-Z0-9_]+$',
                                    message='use slug format',
                                )
                            ]
                            )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', null=True
    )
    rating = models.IntegerField(default=0)
 #   rating = models.ForeignKey(
  #       'Review',
   #      blank=True,
    #     null=True,
     #    on_delete=models.SET_NULL,
      #   related_name='rating',
       #  verbose_name=('Рейтинг'),
     #)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10, message='Оценка должна быть от 1 до 10!'),
            MinValueValidator(1, message='Оценка должна быть от 1 до 10!')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')
        constraints = [models.UniqueConstraint(name='unique_review',
                       fields=['title', 'author'],)]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text
