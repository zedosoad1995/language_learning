from django.db.models import (
    Model, 
    BooleanField, 
    CharField, 
    DateTimeField, 
    IntegerField, 
    PositiveIntegerField, 
    ForeignKey, 
    CASCADE)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone



class User(Model):
    last_update = DateTimeField()
    num_daily_words = PositiveIntegerField(default=3)


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
    is_new = BooleanField(default=False)
