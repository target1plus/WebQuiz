"""WebQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Quiz.views import index, quiz, leaderboard, leaderboard_view, answer

urlpatterns = [
    path('', index, name="index"),
    path('quiz/', quiz, name="quiz"),
    path('answer/', answer, name="answer"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('leaderboard-view/', leaderboard_view, name="leaderboard-view"),
]
