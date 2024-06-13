from django.urls import path
from . import views
urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.login,name="login_page"),
    path("dashboard/",views.dashboard,name="dashboard")
]