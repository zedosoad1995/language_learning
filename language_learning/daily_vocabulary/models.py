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
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    username = CharField(max_length=30, unique=True)
    password = CharField(max_length=20)
    email = EmailField()
    first_name = CharField(max_length=20, null=True)
    last_name = CharField(max_length=30, null=True)
    last_update = DateTimeField(null=True)
    num_daily_words = PositiveIntegerField(default=3)
    timezone = CharField(max_length=30, default='UTC')
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


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
