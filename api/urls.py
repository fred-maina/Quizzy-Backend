# urls.py
from django.urls import path
from .views import quizzes, quiz_detail, questions_by_quiz, create

urlpatterns = [
    path('quizzes/', quizzes, name='quizzes'),
    path('create/',create,name='create'),
    path('quizzes/<str:quiz_code>/', quiz_detail, name='quiz_detail'),  # Update URL pattern to use 'quiz_code'
    path('quizzes/<str:quiz_code>/questions/', questions_by_quiz, name='questions_by_quiz'),
]
