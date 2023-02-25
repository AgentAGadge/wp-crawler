"""
URL definitions for the hyperlist app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_view, name="analyze"),
    path('home/', views.home_view, name="home"),
    path('download_stored_file/', views.download_storage_file_view)
]
