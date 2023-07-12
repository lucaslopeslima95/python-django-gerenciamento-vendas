from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('save_product',views.save_product,name="save_product"),
    path('deactivate_product/<int:id>',views.deactivate_product, name="deactivate_product"),
    path('update_product/<int:id>',views.update_product, name='update_product'),
    path("main_menu_product",views.main_menu_product,name="main_menu_product"),
    path("main_menu_product_with_filter",views.main_menu_product_with_filter,name="main_menu_product_with_filter"),
    path("update_status_product/<int:id>",views.update_status_product,name="update_status_product"),
    path("stock_management/",views.stock_management,name="stock_management"),
    path("stock_management_filter/",views.stock_management_filter,name="stock_management_filter"),
    path("product_movement/<int:id>/",views.product_movement,name="product_movement"),
    path("entry_stock/",views.entry_stock,name="entry_stock"),
    path("transfer_to_store/",views.transfer_to_store,name="transfer_to_store"),
    path("manual_destocking/",views.manual_destocking,name="manual_destocking"),
    path("show_logs_warehouse/",views.show_logs_warehouse,name="show_logs_warehouse"),
    path("show_logs_store_stock/",views.show_logs_store_stock,name="show_logs_store_stock"),
   
]