from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_table, name='display_table'),
    path('athlete/<str:name>/', views.athlete_view, name='athlete_view'),
    path('chart_test/', views.chart_test, name='chart_test')
]