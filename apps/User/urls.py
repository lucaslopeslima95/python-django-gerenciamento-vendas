from django.urls import path
from . import views

app_name ='user'

urlpatterns = [
    path("logout_system",views.logout_system,name="logout_system"),
    path('main_menu_user',views.main_menu_user,name="main_menu_user"),
    path('save_user',views.save_user,name="save_user"),
    path('erase_user/<int:id>', views.erase_user, name='erase_user'),
    path('update_user/<int:id>',views.update_user, name='update_user'),
    path('update_user_password/<int:id>',views.update_user_password, name='update_user_password'),
    path("",views.login_system,name="initial_page"),
    path("page_not_found",views.page_not_found,name="page_not_found")
]
