from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Модель Категорий"""
    title = models.CharField('Название категории', max_length=50)
    slug = models.SlugField('Url', unique=True, max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Название тега', max_length=50)
    slug = models.SlugField('Url', unique=True, max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class SocialLink(models.Model):
    name = models.CharField("Имя соцсети", max_length=15)
    link = models.URLField('Ссылка на соцсеть')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name='Мероприятие')

    def __str__(self):
        return f'{self.name} {self.link}'

    class Meta:
        verbose_name = "Соцсеть"
        verbose_name_plural = "Соцсети"


class Event(models.Model):
    """Модель мероприятия"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    mini_text = models.TextField('Мини текст для превью', max_length=350)
    photo = models.ImageField('Фото для превью', upload_to='photo/%Y/%m/%d/')
    slug = models.SlugField('Url', unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    content = models.TextField('Основной текст', max_length=100000000000)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    edit_date = models.DateTimeField('Дата редактирования', auto_now=True)
    published_date = models.DateTimeField('Дата публикации', default=timezone.now, blank=True, null=True)
    the_date_of_the = models.DateTimeField('Дата проведения', default=timezone.now, blank=True, null=True)
    published = models.BooleanField('Публиковать', default=True)
    number_tickets = models.PositiveIntegerField("Количество билетов")
    location = models.CharField("Место проведения", max_length=100)
    views = models.PositiveIntegerField('Просмотры', default=0)
    tickets_left = models.PositiveIntegerField("Осталось билетов", default=0)

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags.all()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-published_date']


class Ticket(models.Model):
    """Модель билетов"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    name = models.CharField('Имя', max_length=20, blank=True)
    surname = models.CharField('Фамилия', max_length=20, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие', blank=True)
    email = models.EmailField(blank=True)
    published_date = models.DateTimeField('Дата регистрации', auto_now_add=True, blank=True)

    def __str__(self):
        return f'Гость {self.name} идет на {self.event}'

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['-published_date']


class Comment(models.Model):
    """Модель комментариев"""
    name = models.CharField('Имя', max_length=50, blank=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие', blank=True)
    content = models.TextField('Текст комментария', max_length=5000)
    email = models.EmailField(blank=True)
    published_date = models.DateTimeField('Дата публикации', auto_now_add=True, blank=True)

    def __str__(self):
        return f'Автор {self.name} мероприятие {self.event}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-published_date']
