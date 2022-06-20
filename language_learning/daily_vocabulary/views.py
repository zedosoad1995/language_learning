from sqlite3 import Date

from language_learning.settings import TIME_ZONE

from .utils.utils import get_days_since, tz_diff
from .models import User, Word
from .serializers import UserSerializer, WordSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime
from pytz import timezone as py_timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes


@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
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
        data['last_update'] = timezone.now()
        data.setdefault('timezone', TIME_ZONE)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def update_word_scores(request):
    """
    Updates the scores of the words, taking into consideration how much time it has passed since last seeing
    """
    logged_user = User.objects.filter(id=request.auth.get('user_id')).first()
    # TODO: 1o last_update quando a conta foi criada
    last_update = logged_user.last_update

    data = JSONParser().parse(request)
    # TODO: Check timezone is valid
    tz_name = data.get('timezone', logged_user.timezone)
    tz = py_timezone(tz_name)
    now = timezone.now()
    now_to_tz = now.astimezone(tz=tz)

    last_tz_name = logged_user.timezone
    last_tz = py_timezone(last_tz_name)
    last_update = last_update.astimezone(tz=last_tz)

    days_since_max = get_days_since(now_to_tz, last_update)
    if days_since_max <= 0:
        HttpResponse(status=200)

    logged_user.timezone = tz_name
    logged_user.last_update = now
    logged_user.save()

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


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def daily_words_list(request):
    """
    List the top n words of the day, ordered by score (where n is the number of daily words)
    """
    if request.method == 'GET':
        logged_user = User.objects.filter(id=request.auth.get('user_id')).first()
        tz = py_timezone(logged_user.timezone)
        current_date = datetime.now(tz)
        current_day_filter = {
            'created_at_local__date__gte': current_date.date(),
            'created_at_local__time__gte': current_date.time().replace(second=0, microsecond=0) # TODO: remove
        }

        print(current_day_filter)

        num_daily_words = logged_user.num_daily_words
        words = Word.objects.filter(user__id=request.auth.get('user_id'), is_learned=False)\
                .exclude(**current_day_filter)\
                .order_by('-score')[:num_daily_words]

        print(Word.objects.filter(user__id=request.auth.get('user_id'), is_learned=False))

        serializer = WordSerializer(words, many=True)
        return JsonResponse(serializer.data, safe=False)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def words_list(request):
    """
    List words, or create a new word.
    """
    if request.method == 'GET':
        words = Word.objects.filter(user__id=request.auth.get('user_id'))\
                    .order_by('original_word')

        serializer = WordSerializer(words, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['user_id'] = request.auth.get('user_id')
        data['created_at'] = timezone.now()

        serializer = WordSerializer(data=data)
        if serializer.is_valid():
            w = Word(**data)
            w.save()
            return JsonResponse(data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, ])
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


