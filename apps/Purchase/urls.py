from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('save_purchase',views.save_purchase,name="save_purchase"),
    path('find_product',views.find_product,name="find_product")
    ]
