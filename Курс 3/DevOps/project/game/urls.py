from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('play/', views.play, name='play'),
    path('submit-score/', views.submit_score, name='submit_score'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]