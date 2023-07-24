from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('referencial/', views.generate_reports, name='generate_reports'),
    path('consumo_inidividual/', views.make_reports, name="make_reports"),
    path('pagina_inicial_relatorios/', views.page_initial_reports,
         name="page_initial_reports"),
]
