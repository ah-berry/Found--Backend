from django.contrib import admin
from django.urls import path, include
from api.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include((router.urls, 'backend_api'), namespace='backend_api'))
]
