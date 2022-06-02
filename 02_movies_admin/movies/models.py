from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modeified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content\'.\'genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255, unique=True)
    description = models.CharField(_('description'), max_length=4096)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=FilmWorkType.choices, default=FilmWorkType.MOVIE, max_length=255)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file_path'), blank=True, null=True, upload_to='movies/')

    genres = models.ManyToManyField(Genre, through='GenreFilmWork')

    class Meta:
        db_table = 'content\'.\'film_work'
        verbose_name = _('Film')
        verbose_name_plural = _('Films')

    def __str__(self):
        return self.title 


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\'.\'genre_film_work'

    
class Gender(models.TextChoices):

    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=512)
    gender = models.CharField(_('gender'), choices=Gender.choices, max_length=32, null=True)

    films = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content\'.\'person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class PersonFilmWorRole(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=PersonFilmWorRole.choices, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\'.\'person_film_work'
