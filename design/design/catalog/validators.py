from django.core.exceptions import ValidationError

def validate_password_len(password):
    if len(password) < 6:
        raise ValidationError('Длина пароля не может быть меньше 6 символов')