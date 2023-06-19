from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('save_product',views.save_product,name="save_product"),
    path('erase_product/<int:id>',views.erase_product, name="erase_product"),
    path('update_product/<int:id>',views.update_product, name='update_product'),
    path("main_menu_product",views.main_menu_product,name="main_menu_product"),
]