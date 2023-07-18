from django.urls import path

from User.tasks import confirm_register
from . import views
from Purchase.PurchaseService.generateReports import generate_reports

from User.login_logout.login_logout import (
    login_system,
    logout_system
)

app_name ='user'

urlpatterns = [
    path("logout_system",logout_system,name="logout_system"),
    path('main_menu_user',views.main_menu_user,name="main_menu_user"),
    path('save_user',views.save_user,name="save_user"),
    path('erase_user/<int:id>', views.erase_user, name='erase_user'),
    path('update_user/<int:id>',views.update_user, name='update_user'),
    path('update_user_password/<int:id>',views.update_user_password, name='update_user_password'),
    path("",login_system,name="initial_page"),
    path("page_not_found",views.page_not_found,name="page_not_found"),
    path('generate_reports',generate_reports,name='generate_reports'),
    path('main_menu_user_with_filter',views.main_menu_user_with_filter,name="main_menu_user_with_filter"),
    path('page_initial_reports', views.page_initial_reports,name="page_initial_reports"),
    path('make_reports', views.make_reports,name="make_reports"),
    path('confirm_register', confirm_register, name="confirm_register"),
]
