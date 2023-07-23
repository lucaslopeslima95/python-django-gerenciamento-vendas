from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('salvar_categoria', views.save_category, name="save_category"),
    path('atualizar_categoria/<int:id>', views.update_category,
         name='update_category'),
    path("menu_categorias", views.main_menu_category,
         name="main_menu_category"),
]
