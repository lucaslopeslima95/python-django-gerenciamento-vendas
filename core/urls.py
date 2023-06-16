from django.contrib import admin
from django.urls import path,include
from User import urls as User_urls
from Collaborator import urls as collaborator_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(User_urls),name="home"),
    path("collaborator",include(collaborator_urls,namespace="collaborator"),name="collaborator")
]
