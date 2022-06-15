from django.db.models import (
    Model, 
    BooleanField, 
    CharField, 
    DateTimeField,
    FloatField,
    IntegerField, 
    PositiveIntegerField, 
    ForeignKey, 
    CASCADE)
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class User(Model):
    last_update = DateTimeField()
    num_daily_words = PositiveIntegerField(default=3)
    timezone = CharField(max_length=30, default='UTC')


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
