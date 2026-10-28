from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('new/',views.project_create,name='create'),
    path('list/',views.project_list,name='list'),
]