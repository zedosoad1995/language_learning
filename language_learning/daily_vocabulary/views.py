from sqlite3 import Date
from .utils.utils import get_days_since, tz_diff
from .models import User, Word
from .serializers import UserSerializer, WordSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.db.models.functions import Cast
from django.db.models import F, ExpressionWrapper, DateTimeField, IntegerField
from django.utils import timezone
from datetime import datetime
from pytz import timezone as py_timezone


@api_view(['POST'])
def update_word_scores(request):
    """
    Updates the scores of the words, taking into consideration how much time it has passed since last seeing
    """
    current_user = User.objects.first()
    last_update = current_user.last_update

    data = JSONParser().parse(request)
    # TODO: Check timezone is valid
    tz_name = data.get('timezone', current_user.timezone)
    tz = py_timezone(tz_name)
    now = timezone.now()
    now_to_tz = now.astimezone(tz=tz)

    current_user.timezone = tz_name
    current_user.last_update = now
    current_user.save()

    last_tz_name = current_user.timezone
    last_tz = py_timezone(last_tz_name)
    last_update = last_update.astimezone(tz=last_tz)

    days_since_max = get_days_since(now_to_tz, last_update)

    words = Word.objects.filter(is_learned=False)
    for word in words:
        days_since_curr_word = get_days_since(now_to_tz, word.created_at_local.replace(tzinfo=now_to_tz.tzinfo))
        days_since = min(days_since_max, days_since_curr_word)

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
        current_user = User.objects.first()
        tz = py_timezone(current_user.timezone)
        current_date = datetime.now(tz)
        current_day_filter = {
            'created_at_local__date__gte': current_date.date(),
            'created_at_local__time__gte': current_date.time().replace(second=0, microsecond=0) # TODO: remove
        }

        num_daily_words = User.objects.first().num_daily_words
        words = Word.objects.filter(is_learned=False)\
                .exclude(**current_day_filter)\
                .order_by('-score')[:num_daily_words]

        serializer = WordSerializer(words, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['created_at'] = timezone.now()

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
