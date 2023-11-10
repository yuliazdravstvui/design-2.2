from .models import CustomUser, Application
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms

from .validators import validate_password_len


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Фамилия',
                                 validators=[RegexValidator('^[а-яА-Я- -]+$',
                                                            message="Разрешены только кириллица, дефис и пробелы")],
                                 error_messages={'required': 'Обязательное поле',
                                                 })
    last_name = forms.CharField(label='Имя',
                                validators=[RegexValidator('^[а-яА-Я- -]+$',
                                                           message="Разрешены только кириллица, дефис и пробелы")],
                                error_messages={'required': 'Обязательное поле',
                                                })
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-Z0-9-]+$',
                                                          message="Разрешены только латиница, цифры или тире")],
                               error_messages={'required': 'Обязательное поле',
                                               'unique': 'Данный логин занят'
                                               })
    email = forms.EmailField(label='Адрес электронной почты',
                             error_messages={
                                 'invalid': 'Неправильный формат адреса',
                                 'unique': 'Данный адрес занят'
                             })
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               validators=[validate_password_len],
                               error_messages={
                                   'required': ' Обязательное поле',
                               })
    password2 = forms.CharField(label='Пароль(Повторно)',
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': ' Обязательное поле',
                                })
    rules = forms.BooleanField(required=True,
                               label='Согласие с правилами регистрации',
                               error_messages={
                                   'required': ' Обязательное поле',
                               })

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадают', сode='password_mismatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2', 'rules')


class ApplicationForm(forms.ModelForm):
    title = forms.CharField(label='Название проекта', error_messages={'required': 'Обязательное поле'})
    text = forms.CharField(label='Описание проекта', error_messages={'required': 'Обязательное поле'})
    class Meta:
            model = Application
            fields = ('title', 'text', 'category', 'photo_file', 'status', 'date')
