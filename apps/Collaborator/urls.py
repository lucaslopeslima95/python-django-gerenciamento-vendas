from django.urls import path
from . import views

app_name = 'collaborator'

urlpatterns = [
    path('main_menu_user',views.main_menu_user,name="main_menu_user"),
    path('save_collaborator',views.save_collaborator,name="save_collaborator"),
    path('erase_collaborator/<int:id>', views.erase_collaborator, name="erase_collaborator"),
    path('update_collaborator/<int:id>',views.update_collaborator, name='update_collaborator'),
    path('update_collaborator_password/<int:id>',views.update_collaborator_password, name='update_collaborator_password'),
    path("",views.login_system,name="initial_page_collaborator"),
]