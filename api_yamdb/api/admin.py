from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User

# class TitleAdmin(admin.ModelAdmin):
#    list_display = (
#       'pk',
#        'name',
#        'year',
#        'description',
#        'genre',
#        'category',
#    )
#    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)


# admin.site.register(Genre, GenreAdmin)
# admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
