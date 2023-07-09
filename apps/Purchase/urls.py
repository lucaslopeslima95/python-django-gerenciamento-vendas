from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('initial_page_purchase',views.initial_page_purchase,name="initial_page_purchase"),
    path('find_product',views.find_product,name="find_product"),
    path('remove_product_purchase/<int:id>',views.remove_product_purchase,name="remove_product_purchase"),
    path('clean_all_products_purchase',views.clean_all_products_purchase,name="clean_all_products_purchase"),
    path('finish_purchase',views.finish_purchase,name="finish_purchase"),
    path('check_balance',views.check_balance,name="check_balance"),
    path('clean_consult',views.clean_consult,name="clean_consult"),
]