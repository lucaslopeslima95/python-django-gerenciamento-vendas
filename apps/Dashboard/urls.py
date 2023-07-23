from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("pagina_inicial/", views.dashboard, name="dashboard"),
]
