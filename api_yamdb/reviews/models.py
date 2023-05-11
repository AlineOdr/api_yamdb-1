from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

User = get_user_model()


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


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField()
    # rating = models.ForeignKey(
    #     'Review',
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name='rating',
    #     verbose_name=('Рейтинг'),
    # )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

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
            MaxValueValidator(10),
            MinValueValidator(1)
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
