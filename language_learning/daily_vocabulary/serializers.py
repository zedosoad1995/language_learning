from .models import User, Word
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['last_update']


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ['user', 'original_word', 'translated_word', 'knowledge', 'relevance', 'score', 'is_learned', 'is_seen']