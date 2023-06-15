from django.urls import path
from . import views

urlpatterns = [
    path("login_system",views.login_system ,name="login_system"),
    path('logout_system', views.logout_system, name='logout_system'),
    path('main_menu_user',views.main_menu_user,name="main_menu_user"),
    path('save_user',views.save_user,name="save_user"),
    path('erase_user/<int:id>', views.erase_user, name='erase_user'),
    path('update_user/<int:id>',views.update_user, name='update_user'),
    path("",views.initial_page,name="initial_page")
]
