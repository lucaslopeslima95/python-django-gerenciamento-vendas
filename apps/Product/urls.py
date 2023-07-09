from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('save_product',views.save_product,name="save_product"),
    path('deactivate_product/<int:id>',views.deactivate_product, name="deactivate_product"),
    path('update_product/<int:id>',views.update_product, name='update_product'),
    path("main_menu_product",views.main_menu_product,name="main_menu_product"),
    path("main_menu_product_with_filter",views.main_menu_product_with_filter,name="main_menu_product_with_filter"),
    path("update_status_product/<int:id>",views.update_status_product,name="update_status_product")

]