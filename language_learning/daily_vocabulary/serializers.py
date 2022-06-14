from .models import User, Word
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_update', 'num_daily_words']


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'user', 'original_word', 'translated_word', 'knowledge', 'relevance', 'score', 'is_learned', 'is_seen']