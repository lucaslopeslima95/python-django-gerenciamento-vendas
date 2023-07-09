from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('save_category',views.save_category,name="save_category"),
    path('erase_category/<int:id>',views.erase_category, name="erase_category"),
    path('update_category/<int:id>',views.update_category, name='update_category'),
    path("main_menu_category",views.main_menu_category,name="main_menu_category"),
    path("main_menu_category_with_filter",views.main_menu_category_with_filter,name="main_menu_category_with_filter"),
]