from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("gestao_estoque/", views.stock_management, name="stock_management"),
    path("movimentacao_produto/<int:id>/",
         views.product_movement, name="product_movement"),
    path("entrada_estoque/", views.entry_stock, name="entry_stock"),
    path("transferencia_loja/", views.transfer_to_store,
         name="transfer_to_store"),
    path("baixa_manual/", views.manual_destocking, name="manual_destocking"),
    path("historico_deposito/",
         views.show_logs_warehouse, name="show_logs_warehouse"),
    path("historico_loja/",
         views.show_logs_store_stock, name="show_logs_store_stock"),
]
