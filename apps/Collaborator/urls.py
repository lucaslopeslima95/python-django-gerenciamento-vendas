from django.urls import path
from . import views

app_name = 'collaborator'

urlpatterns = [
    path('save_collaborator',views.save_collaborator,name="save_collaborator"),
    path('erase_collaborator/<int:id>', views.erase_collaborator, name="erase_collaborator"),
    path('update_collaborator/<int:id>',views.update_collaborator, name='update_collaborator'),
    path('update_collaborator_password/<int:id>',views.update_collaborator_password, name='update_collaborator_password'),
    path("main_menu_collaborator",views.main_menu_collaborator,name="main_menu_collaborator"),
    path("main_menu_collaborator_with_filter",views.main_menu_collaborator_with_filter,name="main_menu_collaborator_with_filter"),
    path("update_active_collaborator/<int:id>",views.update_active_collaborator,name="update_active_collaborator")
]