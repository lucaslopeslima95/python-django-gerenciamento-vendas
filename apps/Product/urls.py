from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('salvar_produto', views.save_product, name="save_product"),
    path('desativar_produto/<int:id>',
         views.deactivate_product,
         name="deactivate_product"),
    path('atualizar_produto/<int:id>',
         views.update_product, name='update_product'),
    path("menu_produtos",
         views.main_menu_product, name="main_menu_product"),
    path("atualiza_situacao_produto/<int:id>",
         views.update_status_product, name="update_status_product"),
]
