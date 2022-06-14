from django.urls import path
from daily_vocabulary import views

urlpatterns = [
    path('users/', views.user_list),
    path('words/', views.words_list),
    path('words/<int:pk>/', views.word_detail),
    path('words/update', views.update_word_scores),
]