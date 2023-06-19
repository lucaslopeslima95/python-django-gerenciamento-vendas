from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('save_purchase',views.save_purchase,name="save_purchase"),
    path('erase_purchase/<int:id>',views.erase_purchase, name="erase_purchase"),
    path('update_purchase/<int:id>',views.update_purchase, name='update_purchase'),
    path("main_menu_purchase",views.main_menu_purchase,name="main_menu_purchase"),
]