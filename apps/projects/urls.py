from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('new/',views.project_create,name='create'),
    path('list/',views.project_list,name='list'),
    path('<int:pk>/',views.project_detail,name='detail'),
]