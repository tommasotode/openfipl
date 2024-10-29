from django.urls import path
from . import views

urlpatterns = [
    path('table/', views.display_table, name='display_table'),
]