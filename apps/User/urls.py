from django.urls import path

from User.tasks import confirm_register
from . import views


from User.login_logout.login_logout import (
    login_system,
    logout_system
)

app_name = 'user'

urlpatterns = [
    path("", login_system, name="initial_page"),
    path("sair_do_sistema", logout_system, name="logout_system"),
    path('menu_usuarios', views.main_menu_user, name="main_menu_user"),
    path('salvar_usuario', views.save_user, name="save_user"),
    path('excluir_usuario/<int:id>', views.erase_user, name='erase_user'),
    path('atualizar_usuario/<int:id>', views.update_user, name='update_user'),
    path('atualizar_senha_usuario/<int:id>',
         views.update_user_password, name='update_user_password'),
    path("pagina_nao_encontrada", views.page_not_found, name="page_not_found"),
    path('confirmar_registro', confirm_register, name="confirm_register"),
]
