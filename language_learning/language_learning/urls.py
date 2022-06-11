from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from daily_vocabulary.views import UserViewSet, WordViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'words', WordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
