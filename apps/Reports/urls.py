from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('generate_reports/', views.generate_reports, name='generate_reports'),
    path('make_reports/', views.make_reports, name="make_reports"),
    path('page_initial_reports/', views.page_initial_reports,
         name="page_initial_reports"),
]
