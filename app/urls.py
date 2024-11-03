from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_table, name='display_table'),
    path('athlete/<str:name>/', views.athlete_view, name='athlete_view'),
    path('distribution/', views.distribution, name='distribution')
]