from django.db import models
from tinymce.models import HTMLField


class Content(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    state = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', default=0)
    tags = models.ManyToManyField('Tag', verbose_name='Теги', default='')
    introtext = HTMLField(null=True, blank=True, verbose_name='Вступительный текст статьи')
    fulltext = HTMLField(null=True, blank=True, verbose_name='Полный текст статьи')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    publish_up = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Публикация с',
                                      help_text='<span style="color:red;">'
                                                'если оставить поле пустым, то с даты создания</span>')
    publish_down = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Публикация до',
                                        help_text='<span style="color:red;">'
                                                  'если оставить поле пустым, то бессрочно</span>')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', default='', null=True, blank=True, )
    metakey = models.TextField(null=True, blank=True, verbose_name='Meta keywords')
    metadesc = models.TextField(null=True, blank=True, verbose_name='Meta description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['created']


class Category(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'
        ordering = ['name']
