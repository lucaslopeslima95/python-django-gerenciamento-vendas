from django.contrib import admin
from django.urls import path,include
from Usuarios import urls as urls_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(urls_usuario),name="home")
]
