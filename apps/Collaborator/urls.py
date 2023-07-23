from django.urls import path
from . import views

app_name = 'collaborator'

urlpatterns = [
    path('salvar_colaborador', views.save_collaborator,
         name="save_collaborator"),
    path('excluir_colaborador/<int:id>', views.erase_collaborator,
         name="erase_collaborator"),
    path('atualizar_colaborador/<int:id>', views.update_collaborator,
         name='update_collaborator'),
    path('atualizar_senha_colaborador/<int:id>',
         views.update_collaborator_password,
         name='update_collaborator_password'),
    path("menu_colaborador", views.main_menu_collaborator,
         name="main_menu_collaborator"),
    path("atualiza_situacao_colaborador/<int:id>",
         views.update_active_collaborator,
         name="update_active_collaborator")
]
