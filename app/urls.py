from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_table, name='display_table'),
    path('detail/<str:name>/', views.detail_view, name='detail_view'),
]