from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('new/',views.project_create,name='create'),
    path('list/',views.project_list,name='list'),
    path('<int:pk>/',views.project_detail,name='detail'),
    path('<int:pk>/edit/',views.project_edit,name='edit'),
    path('<int:pk>/delete/',views.project_delete,name='delete'),
]