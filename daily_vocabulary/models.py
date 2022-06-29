from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model, 
    BooleanField, 
    CharField, 
    DateTimeField,
    EmailField,
    IntegerField, 
    PositiveIntegerField, 
    ForeignKey, 
    CASCADE)
import re

def validate_username(val):
    if re.fullmatch(r'[a-zA-Z0-9_.]{3,}', val) is None:
        raise ValidationError(
            'Username must have between 1 and 30 characters,' + 
            ' and are only allowed to contain alphanumerics and the symbols . and _'
            )

def validate_password(val):
    if re.fullmatch(
            r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}\[\]:;<>,\.\?\/~_\+\-=|\\])' + 
            r'(?:[a-zA-Z0-9*.!@$%^&(){}\[\]:;<>,\.\?\/~_\+\-=|\\]{8,30})'
            , val
        ) is None:
        raise ValidationError(
            'Password must have between 8 and 30 characters, ' + 
            'contain at least 1 lower case letter, 1 upper case letter, ' + 
            '1 digit and 1 special character'
            )


from .managers import UserManager

NUM_DAILY_WORDS_CHOICES = [(i, i) for i in [1, 3, 5, 10, 15, 20, 50]]


class User(AbstractUser):
    username = CharField(
        max_length=30, 
        unique=True, 
        validators=[validate_username]
        )
    password = CharField(max_length=20, validators=[validate_password])
    email = EmailField()
    first_name = CharField(max_length=20, null=True)
    last_name = CharField(max_length=30, null=True)
    last_update = DateTimeField(null=True)
    num_daily_words = PositiveIntegerField(default=3, choices=NUM_DAILY_WORDS_CHOICES)
    timezone = CharField(max_length=30, default='UTC')
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str({k: getattr(self, k) for k in User().__dict__.keys() if not k.startswith('_')})


class Word(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    original_word = CharField(max_length=100)
    translated_word = CharField(max_length=350)
    knowledge = IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    relevance = IntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    score = PositiveIntegerField(default=0)
    is_learned = BooleanField(default=False)
    is_seen = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.fromtimestamp(0))
    created_at_local = DateTimeField(default=datetime.fromtimestamp(0))
