from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('save_purchase',views.save_purchase,name="save_purchase"),
    path('find_product',views.find_product,name="find_product"),
    path('remove_product_purchase/<int:id>',views.remove_product_purchase,name="remove_product_purchase"),
    path('clean_all_products_purchase',views.clean_all_products_purchase,name="clean_all_products_purchase"),
    ]
