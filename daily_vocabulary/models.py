from datetime import datetime
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
from pytz import timezone as py_timezone

from .validators import (
    validate_username, 
    validate_at_least_one_lower_case,
    validate_at_least_one_upper_case,
    validate_at_least_one_digit,
    validate_at_least_one_special_character,
    validate_password_length
)


from .managers import UserManager

NUM_DAILY_WORDS_CHOICES = [(i, i) for i in [1, 3, 5, 10, 15, 20, 50]]


class User(AbstractUser):
    username = CharField(
        max_length=30, 
        unique=True, 
        validators=[validate_username]
        )
    password = CharField(max_length=300, validators=[
        validate_at_least_one_lower_case,
        validate_at_least_one_upper_case,
        validate_at_least_one_digit,
        validate_at_least_one_special_character,
        validate_password_length
        ])
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
    created_at = DateTimeField(default=datetime.fromtimestamp(0, py_timezone('UTC')))
    created_at_local = DateTimeField(default=datetime.fromtimestamp(0, py_timezone('UTC')))

    def __str__(self):
        return self.original_word
