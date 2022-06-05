from django.contrib import admin
from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
    list_display = ('full_name',)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmWorkInline,
        PersonFilmWorkInline,
    )

    list_display = (
        'title',
        'description',
        'creation_date',
        # 'get_director',
        # 'get_actors',
        'type',
        'rating',
    )
    list_filter = (
        'type',
        'creation_date',
        'genres__name',
    )
    search_fields = ('title', 'genres__name')

    # @display
    # def get_director(self, obj):
