from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_view, name='display_table'),
    path('athlete/<str:name>/', views.athlete_view, name='athlete_view'),
]