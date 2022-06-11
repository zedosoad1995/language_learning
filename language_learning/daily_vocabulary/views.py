from .models import User, Word
from rest_framework import permissions, viewsets
from .serializers import UserSerializer, WordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    num_daily_words = User.objects.first().num_daily_words
    queryset = Word.objects.order_by('-score')[:num_daily_words]
    serializer_class = WordSerializer
