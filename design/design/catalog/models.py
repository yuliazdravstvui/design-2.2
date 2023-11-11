from django import utils
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator
from django.template.backends import django
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    username = models.CharField(max_length=254, verbose_name='Лoгин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Пoчтa', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пapoль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пoльзователь')), default='user')


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Нaименование', blank=False)

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('N', 'Новая'),
        ('P', 'Принято в работу'),
        ('C', 'Выполнено'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Введите краткое описание заявки")
    category = models.ForeignKey(Category, help_text="Выберите категорию заявки", on_delete=models.CASCADE, default='0')

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    photo_file = models.ImageField(max_length=254, upload_to='image/', validators=[validate_image, FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])])
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES, default='N')
    date = models.DateTimeField(verbose_name='Дата добавления', null=True, auto_now_add=True)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('application_list', args=[str(self.id)])

    def __str__(self):
        return self.title
