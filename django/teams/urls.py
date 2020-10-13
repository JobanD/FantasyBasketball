from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='team-index'),
    path('<team_id>/', views.detail, name='team-detail'),
]