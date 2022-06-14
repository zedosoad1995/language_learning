from .models import User, Word
from .serializers import UserSerializer, WordSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.utils import timezone


@api_view(['POST'])
def update_word_scores(request):
    """
    Updates the scores of the words, taking into consideration how much time it has passed since last seeing
    """
    current_user = User.objects.first()
    last_update = current_user.last_update
    last_update = last_update.replace(second=0, microsecond=0)

    current_datetime = timezone.now()
    current_user.last_update = current_datetime
    current_user.save()

    current_datetime = current_datetime.replace(second=0, microsecond=0)

    days_since = (current_datetime - last_update).total_seconds() / 60.0
    print(days_since)

    words = Word.objects.filter(is_learned=False)
    for word in words:
        if days_since > 0:
            if word.is_seen:
                word.score = 0
                word.is_seen = False
            else:
                word.score += days_since * (word.relevance + 6 - word.knowledge)

            word.is_new = False

        word.save()

    return HttpResponse(status=200)


@api_view(['GET', 'POST'])
def words_list(request):
    """
    List words, or create a new word.
    """
    if request.method == 'GET':
        num_daily_words = User.objects.first().num_daily_words
        words = Word.objects.filter(is_learned=False, is_new=False).order_by('-score')[:num_daily_words]
        serializer = WordSerializer(words, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
def word_detail(request, pk):
    """
    Retrieve, update or delete a word.
    """
    try:
        word = Word.objects.get(pk=pk)
    except Word.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = WordSerializer(word)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = WordSerializer(word, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        word.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
