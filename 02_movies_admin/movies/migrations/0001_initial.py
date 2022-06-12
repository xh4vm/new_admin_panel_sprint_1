# Generated by Django 3.2 on 2022-06-12 16:33

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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.CharField(max_length=4096, verbose_name='description')),
                ('creation_date', models.DateField(verbose_name='creation_date')),
                ('file_path', models.CharField(blank=True, default='', max_length=4096, verbose_name='file_path')),
                (
                    'rating',
                    models.FloatField(
                        null=True,
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
            ],
            options={'verbose_name': 'Film', 'verbose_name_plural': 'Films', 'db_table': 'content"."film_work', },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={'verbose_name': 'Genre', 'verbose_name_plural': 'Genres', 'db_table': 'content"."genre', },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=512, verbose_name='full_name')),
            ],
            options={'verbose_name': 'Person', 'verbose_name_plural': 'Persons', 'db_table': 'content"."person', },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    'role',
                    models.CharField(
                        choices=[('actor', 'Actor'), ('writer', 'Writer'), ('director', 'Director')],
                        max_length=255,
                        verbose_name='role',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='Film Work'
                    ),
                ),
                (
                    'person',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='Person'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='films',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.FilmWork'),
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='Film Work'
                    ),
                ),
                (
                    'genre',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='Genre'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(related_name='films', through='movies.GenreFilmWork', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.Person'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work', 'person', 'role'], name='person_film_film_wo_6b9cac_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work', 'genre'], name='genre_film__film_wo_399489_idx'),
        ),
    ]
