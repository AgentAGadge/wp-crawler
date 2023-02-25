"""
URL definitions for the hyperlist app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.AnalyzeView.as_view(), name="analyze"),
    path('home/', views.HomeView.as_view(), name="home"),
    path('download_stored_file/', views.DownloadStorageFileView.as_view())
]
