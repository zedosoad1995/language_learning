from .models import User, Word
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'timezone', 'last_update', 'num_daily_words', 'is_staff', 'is_superuser', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_date):
        password = validated_date.pop('password', None)
        instance = self.Meta.model(**validated_date)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'original_word', 'translated_word', 'knowledge', 'relevance', 'score', 'is_learned', 'is_seen', 'created_at_local', 'created_at']