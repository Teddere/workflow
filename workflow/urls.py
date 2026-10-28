
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.dashboard.urls',namespace='dashboard')),
    path('', include('apps.account.urls',namespace='account')),
    path('projects/',include('apps.projects.urls',namespace='projects')),
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
