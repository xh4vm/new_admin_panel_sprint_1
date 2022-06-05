# Generated by Django 3.2 on 2022-06-03 17:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modeified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('description', models.CharField(max_length=4096, verbose_name='description')),
                ('creation_date', models.DateField(verbose_name='creation_date')),
                (
                    'rating',
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name='rating',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[('movie', 'Movie'), ('tv_show', 'TV Show')],
                        default='movie',
                        max_length=255,
                        verbose_name='type',
                    ),
                ),
                (
                    'certificate',
                    models.CharField(blank=True, max_length=512, verbose_name='certificate'),
                ),
                (
                    'file_path',
                    models.FileField(
                        blank=True, null=True, upload_to='movies/', verbose_name='file_path'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Film',
                'verbose_name_plural': 'Films',
                'db_table': "content'.'film_work",
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modeified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': "content'.'genre",
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modeified', models.DateTimeField(auto_now=True)),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('full_name', models.CharField(max_length=512, verbose_name='full_name')),
                (
                    'gender',
                    models.CharField(
                        choices=[('male', 'Male'), ('female', 'Female')],
                        max_length=32,
                        null=True,
                        verbose_name='gender',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'db_table': "content'.'person",
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    'role',
                    models.CharField(
                        choices=[('actor', 'Actor'), ('director', 'Director')],
                        max_length=255,
                        verbose_name='role',
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'
                    ),
                ),
                (
                    'person',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.person'
                    ),
                ),
            ],
            options={'db_table': "content'.'person_film_work", },
        ),
        migrations.AddField(
            model_name='person',
            name='films',
            field=models.ManyToManyField(
                through='movies.PersonFilmWork', to='movies.FilmWork'
            ),
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'
                    ),
                ),
                (
                    'genre',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.genre'
                    ),
                ),
            ],
            options={'db_table': "content'.'genre_film_work", },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.Genre'),
        ),
    ]
