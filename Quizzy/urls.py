from django.urls import path
from . import views
urlpatterns=[
    path("",views.index,name="index"),
    path("login/",views.login,name="login_page"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("add/",views.add,name="add_quiz"),
    path('quiz/<str:quiz_code>/', views.display_quiz, name='display')
]