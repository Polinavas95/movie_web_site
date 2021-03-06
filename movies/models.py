from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Жанр', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField('Название', max_length=100)
    tag_line = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveIntegerField('Год выпуска', default=2000)
    country = models.CharField('Страна', max_length=100)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актер', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанр', related_name='film_genre')
    world_premier = models.DateField('Премьера', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Укажите сумму в долларах')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='Укажите сумму в долларах')
    fees_in_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='Укажите сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    """Рейтинг фильма"""
    value = models.SmallIntegerField('Рейтинг', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Рейтинг фильма'
        verbose_name_plural = 'Рейтинги фильма'


class Rating(models.Model):
    """Рейтинг фильма"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Рейтинг')
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name='Фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Rewies(models.Model):
    """Отзывы к фильму"""
    email = models.EmailField()
    name = models.CharField('Отзыв', max_length=100)
    text = models.TextField('Текст сообщения', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв к фильму'
        verbose_name_plural = 'Отзывы к фильму'
